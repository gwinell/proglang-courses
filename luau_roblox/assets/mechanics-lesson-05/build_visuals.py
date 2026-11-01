"""Original lesson 5 diagrams. Uses the shared vector primitives from lesson 4."""
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('lesson_vectors', HERE.parent / 'objects-lesson-04' / 'build_visuals.py')
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)
text, box, line = G.text, G.box, G.line
BLUE, GREEN, ORANGE, PURPLE = G.BLUE, G.GREEN, G.ORANGE, G.PURPLE

def wrap(title, subtitle, content, footer='Учебная схема • Roblox Studio • урок 5'):
    return G.wrap(title, subtitle, content, footer)

def scope():
    s = box(48,150,535,360,stroke=BLUE) + box(615,150,537,360,stroke=ORANGE)
    s += text(76,196,'Состояние игрока',29,BLUE,700)
    s += text(644,196,'Состояние предмета',29,ORANGE,700)
    for x,y,name,coins,stage,deadline in [(76,230,'A',5,1,'2.0'),(76,365,'B',0,0,'0.0')]:
        s += box(x,y,475,115,fill='#eff5ff',stroke='#bfd1f0')
        s += text(x+18,y+35,'Игрок '+name,23,weight=700)
        s += text(x+18,y+72,f'coins = {coins}   •   stage = {stage}',22)
        s += text(x+18,y+101,'nextDamageAt = '+deadline,20,G.MUTED)
    for y,name,value,color in [(230,'Coin1','false',ORANGE),(365,'Coin2','true',GREEN)]:
        s += box(644,y,478,115,fill='#fff8ec',stroke='#e9d1a4')
        s += text(665,y+40,name,25,weight=700)
        s += text(665,y+83,'available = '+value,25,color,700)
    s += text(48,560,'Урон: пауза одного игрока не блокирует другого.',24,weight=700)
    s += text(48,600,'Монета: после подбора предмет временно недоступен всем.',23,G.MUTED)
    return wrap('У защиты есть область действия', 'Разные механики требуют разных ключей состояния.',s)

def checkpoints():
    s=''
    for y,name,stage in [(175,'A',2),(380,'B',1)]:
        s += box(48,y,520,150,stroke=BLUE)
        s += text(76,y+43,'Игрок '+name,28,BLUE,700)
        s += text(76,y+86,'Stage = '+str(stage),25)
        s += text(76,y+125,'RespawnLocation → Checkpoint'+str(stage),22,G.MUTED)
        s += box(785,y,367,150,stroke=GREEN,fill='#eff8f4')
        s += text(810,y+62,'Checkpoint'+str(stage),30,GREEN,700)
        s += text(810,y+108,'SpawnLocation',23,G.MUTED)
        s += line(582,y+75,768,y+75)
    s += text(48,590,'Один мир, но место следующего появления у каждого своё.',23,weight=700)
    return wrap('Контрольная точка принадлежит игроку', 'Стрелки показывают ссылки, а не маршрут движения персонажа.',s)

def lifecycle():
    s=''
    rows=[(175,'Монета',BLUE,[('Есть Part','available = true'),('Принять касание','Coins + 5'),('Скрыть на 4 с','available = false'),('Показать снова','тот же объект')]),
          (395,'Аптечка',GREEN,[('Есть предмет','здоровье < Max'),('Восстановить','до MaxHealth'),('Destroy + 6 с','предмета нет'),('Создать снова','новый объект')])]
    for y,title,color,cards in rows:
        s += text(48,y-20,title,27,color,700)
        for i,(a,b) in enumerate(cards):
            x=48+i*286;s+=box(x,y,246,140,stroke=color)
            s+=text(x+16,y+49,a,21,G.INK,700)
            s+=text(x+16,y+97,b,20,G.MUTED)
            if i<3:s+=line(x+251,y+70,x+278,y+70)
    return wrap('Возвращение предметов в мир', 'Спрятать существующий объект и создать новый — разные жизненные циклы.',s)

def coin_frame(t):
    phase=min(int(t*6),5)
    available=phase in [0,4]
    a=0 if phase==0 else 5
    b=5 if phase==5 else 0
    captions=['Готово: оба игрока видят монету','Первым обработан A: он получает 5 монет','Монета скрыта, подключение Touched сохранено','Повторные касания игнорируются','Через 4 секунды тот же Part снова доступен','Теперь B подбирает монету: у него тоже 5']
    s=box(48,150,1104,435)
    for x,name,value,color in [(200,'A',a,BLUE),(1000,'B',b,PURPLE)]:
        s+=f'<circle cx="{x}" cy="285" r="65" fill="#e9efff" stroke="{color}" stroke-width="4"/>'
        s+=text(x,300,name,48,color,700,'middle')
        s+=text(x,402,'Coins = '+str(value),28,color,700,'middle')
    if available:
        s+='<circle cx="600" cy="285" r="66" fill="#f8cc4d" stroke="#be8b13" stroke-width="4"/>'
        s+=text(600,303,'5',50,'#73520c',700,'middle')
    else:
        s+='<circle cx="600" cy="285" r="66" fill="#f4f7fc" stroke="#b9c5d7" stroke-width="3" stroke-dasharray="10 8"/>'
        s+=text(600,295,'скрыта',22,G.MUTED,anchor='middle')
    s+=text(600,408,'available = '+str(available).lower(),27,GREEN if available else ORANGE,700,'middle')
    s+=text(600,486,captions[phase],25,G.INK,700,'middle')
    s+=text(600,541,'Один принятый подбор — одна награда.',23,G.MUTED,anchor='middle')
    return wrap('Одна монета, два игрока', 'Флаг меняем до начисления награды и до запуска таймера.',s,
        'Учебная модель, не запись Studio. Повтор GIF начинает новый демонстрационный опыт.')

if __name__=='__main__':
    for name,svg in [('04-state-scope.svg',scope()),('05-checkpoints.svg',checkpoints()),('06-pickup-cycle.svg',lifecycle())]:
        (HERE/name).write_text(svg)
    frames=HERE/'_frames/07-coin-cycle';frames.mkdir(parents=True,exist_ok=True)
    for i in range(36):(frames/f'{i:03}.svg').write_text(coin_frame(i/36))
    print('Created 3 SVG diagrams and 36 animation frames.')
