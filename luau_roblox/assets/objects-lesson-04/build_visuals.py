"""Create the lesson's original SVG diagrams and SVG animation frames.

No external raster artwork is modified. SVG frames are rendered to PNG by the
companion renderer, then assembled into GIF by that renderer's Python step.
"""
from pathlib import Path
from html import escape

HERE = Path(__file__).resolve().parent
WIDTH, HEIGHT = 1200, 680
BG, INK, MUTED = '#f4f7fc', '#17243d', '#52627c'
BLUE, GREEN, ORANGE, PURPLE = '#2563eb', '#0f8a68', '#d96b19', '#7550cc'

def text(x, y, value, size=24, fill=INK, weight=400, anchor='start'):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'

def box(x, y, w, h, fill='white', stroke='#d7e0ed', radius=18):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'

def line(x1, y1, x2, y2, color=BLUE, dashed=False):
    dash = ' stroke-dasharray="8 7"' if dashed else ''
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="4" marker-end="url(#arrow)"{dash}/>'

def wrap(title, subtitle, content, footer='Учебная схема • Luau / Roblox Studio • урок 4'):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="{escape(title)}">
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="none" stroke="{BLUE}" stroke-width="1.4"/></marker></defs>
<style>text{{font-family:Arial,Helvetica,sans-serif}}svg{{background:{BG}}}</style>
<rect width="1200" height="680" fill="{BG}"/>
{text(48,65,title,36,weight=700)}{text(48,104,subtitle,21,MUTED)}
{content}
{text(48,650,footer,18,MUTED)}
</svg>'''

def hierarchy():
    s = box(48,145,690,450)
    for x,y,w,label,color in [
        (78,170,220,'Workspace',BLUE),(118,250,250,'Lesson04Control',PURPLE),
        (168,350,220,'Control',BLUE),(208,450,260,'ProximityPrompt',ORANGE),
        (438,350,220,'Cube',GREEN),(478,450,220,'PointLight',ORANGE),
    ]:
        s += box(x,y,w,58,fill='#f8fbff',stroke=color,radius=12) + text(x+18,y+37,label,24,weight=700)
    s += line(120,228,155,250) + line(195,308,220,350) + line(335,308,490,350)
    s += line(245,408,260,450) + line(555,408,570,450)
    s += box(770,145,382,450)
    s += text(794,190,'У каждого объекта',25,weight=700) + text(794,223,'только один Parent',25,weight=700)
    for i,v in enumerate(['Для Lesson04Control:', 'Control и Cube — дети.', 'Prompt и PointLight —', 'потомки, но не дети.', '', 'GetChildren(): 2', 'GetDescendants(): 4']):
        s += text(794,275+i*39,v,22,BLUE if i>=5 else INK)
    return wrap('Иерархия: дети и потомки', 'Стрелка идёт от родителя к дочернему объекту. Это не карта координат.',s)

def event_flow():
    s = ''
    cards=[('01','Действие','Игрок нажимает E',BLUE),('02','Событие','Triggered(player)',PURPLE),('03','Обработчик','onTriggered',ORANGE),('04','Результат','Cube создан',GREEN)]
    for i,(n,title,caption,color) in enumerate(cards):
        x=48+i*286
        s+=box(x,190,246,185,stroke=color)
        s+=text(x+22,228,n,20,color,700)+text(x+22,275,title,26,weight=700)+text(x+22,325,caption,19,MUTED)
        if i<3:s+=line(x+251,282,x+279,282)
    s+=box(48,420,1104,164,fill='#eaf0ff',stroke='#b9cafa')
    s+=text(76,463,'Подключение выполняется один раз:',24,weight=700)
    s+=text(76,507,'prompt.Triggered:Connect(onTriggered)',29,BLUE,700)
    s+=text(76,550,'Передаём функцию без (). Она выполнится позже, когда придёт событие.',21,MUTED)
    return wrap('От действия к обработчику', 'Событие передаёт аргументы. Обработчик читает их и меняет состояние мира.',s)

def lifecycle():
    s=''
    for x,title,code,color,notes in [
        (48,'1. Создать','Instance.new("Part")',BLUE,['Объект есть в переменной.','Parent пока равен nil.']),
        (430,'2. Добавить в мир','part.Parent = folder',GREEN,['Сначала задать свойства.','Затем назначить Parent.']),
        (812,'3. Уничтожить','part:Destroy()',ORANGE,['Удаляются и потомки.','Объект нельзя вернуть.']),
    ]:
        s+=box(x,175,340,270,stroke=color)
        s+=text(x+22,221,title,27,color,700)+text(x+22,278,code,21,INK,700)
        s+=text(x+22,334,notes[0],21)+text(x+22,372,notes[1],21)
    s+=line(392,307,421,307)+line(774,307,803,307)
    s+=box(48,482,1104,110,fill='#fff5e9',stroke='#efcba6')
    s+=text(72,525,'Parent = nil — временно убрать из дерева, сохранив ссылку.',24,weight=700)
    s+=text(72,563,'Destroy() — завершить жизнь объекта. После этого переменную лучше обнулить.',21,MUTED)
    return wrap('Жизненный цикл объекта', 'Создание, появление в дереве и уничтожение — разные действия.',s)

def reparent_frame(t):
    # 0..1: one logical parent changes; there is no claim of 3D movement.
    moved=t>=.52
    s=box(48,145,1104,445)
    s+=box(120,190,320,80,stroke=BLUE)+text(280,240,'Inbox',30,BLUE,700,'middle')
    s+=box(760,190,320,80,stroke=PURPLE)+text(920,240,'Archive',30,PURPLE,700,'middle')
    x=220 if not moved else 860
    if .3<t<.52:
        x=220+(t-.3)/.22*640
    s+=box(x-85,340,170,80,fill='#e4f5ef',stroke=GREEN)+text(x,390,'Token',28,GREEN,700,'middle')
    if not (.3<t<.52):s+=line(280 if not moved else 920,277,x,332)
    s+=box(120,465,960,74,fill='#eaf0ff',stroke='#b9cafa')
    s+=text(600,513,'token.Parent = archive' if t>=.3 else 'token.Parent = inbox',30,BLUE,700,'middle')
    status='После: Token — ребёнок Archive' if moved else 'До: Token — ребёнок Inbox'
    s+=text(600,574,status,24,INK,700,'middle')
    return wrap('Меняем Parent — меняем дерево', 'Анимация показывает связь объектов. Position у детали остаётся прежним.',s)

def event_frame(t):
    phase=min(int(t*6),5)
    busy=phase in [1,4]
    cube=phase in [1,2,3]
    labels=['Готово к нажатию','Обработчик: создать Cube','Пауза завершена','Второе нажатие','Обработчик: удалить Cube','Снова исходное состояние']
    s=box(48,145,520,445)+box(600,145,552,445)
    s+=text(78,190,'Схема сцены',25,weight=700)
    s+=box(108,270,170,140,fill='#dbeafe',stroke=BLUE)+text(193,330,'Пульт',26,BLUE,700,'middle')
    s+=box(138,350,110,44,fill='#fff',stroke=BLUE,radius=10)+text(193,380,'E',28,BLUE,700,'middle')
    if cube:
        s+='<path d="M380,273 l65,-35 l65,35 v90 l-65,35 l-65,-35 z" fill="#b8eddb" stroke="#0f8a68" stroke-width="3"/>'
        s+='<path d="M380,273 l65,35 l65,-35 M445,308 v90" fill="none" stroke="#0f8a68" stroke-width="3"/>'
        s+=text(445,443,'Cube',25,GREEN,700,'middle')
    else:s+=text(438,340,'Куба нет',24,MUTED,anchor='middle')
    s+=text(78,490,labels[phase],21,INK,700)
    s+=text(78,535,'Пауза 1 с: новые срабатывания не принимаем.' if busy else 'Можно взаимодействовать с пультом.',19,MUTED)
    s+=text(634,192,'Состояние обработчика',25,weight=700)
    for i,(label,value) in enumerate([('busy',str(busy).lower()),('prompt.Enabled',str(not busy).lower()),('activeCube','Cube' if cube else 'nil')]):
        y=235+i*91;s+=box(630,y,490,68,fill='#fff5e9' if busy and i<2 else '#eff7f3',stroke='#efcba6' if busy and i<2 else '#b7daca')
        s+=text(650,y+42,label,23,INK,700)+text(1096,y+42,value,23,ORANGE if busy and i<2 else GREEN,700,'end')
    s+=text(634,555,'busy ставим до task.wait(1)',22,MUTED)
    return wrap('Событие → действие → пауза', 'Две активации пульта. Это учебная анимация, а не запись экрана Studio.',s)

def main():
    HERE.mkdir(exist_ok=True)
    for name,content in [('05-hierarchy.svg',hierarchy()),('06-event-flow.svg',event_flow()),('07-lifecycle.svg',lifecycle())]:
        (HERE/name).write_text(content)
    frames=HERE/'_frames'
    frames.mkdir(exist_ok=True)
    for name,func in [('08-reparent',reparent_frame),('09-event-cooldown',event_frame)]:
        folder=frames/name;folder.mkdir(exist_ok=True)
        for i in range(36):
            (folder/f'{i:03}.svg').write_text(func(i/36))
    print('Created 3 SVG diagrams and 72 source frames for two GIFs.')

if __name__=='__main__':
    main()
