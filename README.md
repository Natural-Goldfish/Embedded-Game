# **Introduction**

본 프로젝트는 Raspberry Pi 4에서 Python으로 구현한 shooting game입니다.

</br></br>

# **Requirements**

- Raspberry Pi 4
- Adafruit 1.3 Color TFT Bonnet for Raspberry Pi
- Python 3.7.3

</br></br>

# Project Structure

```
    Shooting-Game
    ├──images
    │   ├──background.png
    │   ├──...
    │   ├──effect-boom1.png
    │   ├──...
    │   ├──enemy1.png
    │   ├──...
    │   ├──missile1.png
    │   ├──...
    │   ├──player1.png
    │   ├──...
    │   ├──player-missile1.png
    │   └──...
    ├──src
    │   ├──__init__.py
    │   ├──background.py
    │   ├──button.py
    │   ├──game_objects.py
    │   ├──object_controller.py
    │   └──game_starter.py
    ├──__init__.py
    ├──settings.py
    └──main.py  
```

</br></br>

# Objects
  게임 객체는 화면에 게임 진행에 필요한 _**game object**_ 와 display되는 부분을 담당하는 _**background object**_ 로 구분됩니다.  

  </br>

  - ## Game Object
    _**Game object**_ 는 게임 진행에 필요한 객체를 의미하며, 관련 내용은 `src/game_objects.py`에 정의되어 있습니다. 게임에 사용되는 모든 객체들에 대한 정보는 _**OBJECT_INFO**_ 에 있으며, 모든 객체들은 _GameObject_ 를 상속합니다. _GameObject_ 는 아래와 같은 속성들을 가지고 있습니다.  

    _**name**_ 은 _OBJECT_INFO_ 에서 가져올 object의 이름을 의미합니다.  

    _**team**_ 은 object가 속한 집단을 의미합니다. 

    _**role**_ 은 object가 수행하는 역할을 의미합니다.  

    _**speed**_ 는 display가 갱신될 때, object가 이동하게 되는 x축과 y축의 변화량을 의미합니다.  

    _**image**_ 는 object의 image를 의미합니다.  

    _**width, height**_ 는 image의 가로와 세로 크기를 의미합니다.  

    _**obj_coord**_ 는 object의 중심 좌표를 의미합니다.  

    _**image_coord**_ 는 object의 중심 좌표에 image를 load했을 때, 좌상단 좌표와 우하단 좌표를 의미합니다.  

    _**obj_id**_ 는 object의 고유한 identification을 의미합니다.  

    </br>

    - ### Enemy Object and Missile Object
      _**Enemy object**_ 는 player가 격추해야 하는 적군 전투기를 의미합니다. _**Missile object**_ 는 적군 전투기가 사용하는 missile 객체를 의미하며, _enemy<sub>i</sub>_ 는 _missile<sub>i</sub>_ 를 사용합니다. 모든 enemy 객체는 체력을 의미하는 _hp_ 와 공격 주기를 의미하는 _attack_cycle_ 를 가지고 있습니다.  
      
      <div align='center'>
  
      |Index|Fighter Plane|HP|Attack Cycle (Sec)|Missile|Damage|
      |:---:|:---:|:---:|:---:|:---:|:---:|
      |1|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/enemy1.png" alt="enemy1" width="50" height="50" />|10|3|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/missile1.png?raw=true" alt="missile1" width="50" height="50" />|11|
      |2|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/enemy2.png?raw=true" alt="enemy2" width="50" height="50" />|13|3|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/missile2.png?raw=true" alt="missile2" width="50" height="50" />|13|
      |3|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/enemy3.png?raw=true" alt="enemy3" width="50" height="50" />|15|2.5|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/missile3.png?raw=true" alt="missile3" width="50" height="50" />|15|
      |4|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/enemy4.png?raw=true" alt="enemy4" width="50" height="50" />|17|2|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/missile4.png?raw=true" alt="missile4" width="50" height="50" />|17|
      |5|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/enemy5.png?raw=true" alt="enemy5" width="50" height="50" />|20|1.5|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/missile5.png?raw=true" alt="missile5" width="50" height="50" />|20|
  
      </div>
      
    </br>
      
    - ### Player Object and Player-Missile Object
      _**Player object**_ 는 player가 사용하는 전투기를 의미합니다. _**Player-Missile object**_ 는 player 전투기가 사용하는 missile 객체를 의미하며, _player<sub>i</sub>_ 는 _player-missile<sub>i</sub>_ 를 사용합니다. _Player object_ 는 체력을 의미하는 _hp_ 와 격추한 적군 전투기의 개수를 의미하는 _kill_point_ 를 가지고 있습니다.

    </br>

    - ### Effect-Boom object
      _**Effect-Boom object**_ 는 전투기가 공격받고 폭파되는 경우 생성되는 effect 객체입니다.

  </br>

  - ## Background Object
    _**Background object**_ 는 배경화면을 display하는 객체를 의미하며, 관련 내용은 `src/background.py`에 정의되어 있습니다. 모든 background object와 관련된 정보는 _**BACKGROUND_INFO**_ 에 있습니다. 앞서 설명한 game object의 이미지는 background object가 _call_ 됐을 때, background object가 가진 배경 이미지에 덧붙여집니다.

</br></br>

# Object Controller

</br></br>

# Game Starter

</br></br>

