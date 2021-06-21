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
본 프로젝트에서 사용되는 객체는 크게 _**game object**_ 와 _**background object**_ 로 구분됩니다.  

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
  
      |Index|Fighter Plane|HP|Speed(x, y)|Attack Cycle(Sec)|Missile|Damage|
      |:---:|:---:|:---:|:---:|:---:|:---:|:---:|
      |1|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/enemy1.png" alt="enemy1" width="60" height="60" />|10|(1, 1)|3|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/missile1.png?raw=true" alt="missile1" width="60" height="60" />|11|
      |2|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/enemy2.png?raw=true" alt="enemy2" width="60" height="60" />|13|(-2, 2)|3|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/missile2.png?raw=true" alt="missile2" width="60" height="60" />|13|
      |3|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/enemy3.png?raw=true" alt="enemy3" width="60" height="60" />|15|(-3, 1)|2.5|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/missile3.png?raw=true" alt="missile3" width="60" height="60" />|15|
      |4|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/enemy4.png?raw=true" alt="enemy4" width="60" height="60" />|17|(-4, 1)|2|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/missile4.png?raw=true" alt="missile4" width="60" height="60" />|17|
      |5|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/enemy5.png?raw=true" alt="enemy5" width="60" height="60" />|20|(-5, 2)|1.5|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/missile5.png?raw=true" alt="missile5" width="60" height="60" />|20|
  
      </div>
      
    </br>
      
    - ### Player Object and Player-Missile Object
      _**Player object**_ 는 player가 사용하는 전투기를 의미합니다. _**Player-Missile object**_ 는 player 전투기가 사용하는 missile 객체를 의미하며, _player<sub>i</sub>_ 는 _player-missile<sub>i</sub>_ 를 사용합니다. _Player object_ 는 체력을 의미하는 _hp_ 와 격추한 적군 전투기의 개수를 의미하는 _kill_point_ 를 가지고 있습니다.

      <div align='center'>
      
      |Index|Fighter Plane|HP|Speed(x, y)|Missile|Damage|
      |:---:|:---:|:---:|:---:|:---:|:---:|
      |1|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/player1.png?raw=true" alt="player1" width="60" height="60"/>|20|(10, 10)|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/player-missile1.png?raw=true" alt="player-missile1" width="60" height="60"/>|15|
    
      </div>
      
    </br>

    - ### Effect-Boom object
      _**Effect-Boom object**_ 는 전투기가 공격받고 폭파되는 경우 생성되는 effect 객체입니다.

      <div align='center'>
      
      |Index|Effect Boom|
      |:---:|:---:|
      |1|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/effect-boom1.png?raw=true" alt="effect-boom1" width="60" height="60"/>|
    
      </div>

  </br>

  - ## Background Object
    _**Background object**_ 는 배경화면을 display하는 객체를 의미하며, 관련 내용은 `src/background.py`에 정의되어 있습니다. 모든 background object와 관련된 정보는 _**BACKGROUND_INFO**_ 에 있습니다. 앞서 설명한 game object의 이미지는 background object가 _call_ 됐을 때, background object가 가진 배경 이미지에 덧붙여집니다.

      <div align='center'>
      
      |Index|Background|
      |:---:|:---:|
      |1|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/background.png?raw=true" alt="background1" width="120" height="120"/>|
      |2|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/background2.png?raw=true" alt="background2" width="120" height="120"/>|
    
      </div>

</br></br>

# Object Controller
_**Object controller**_ 는 본 프로젝트에서 정의된 모든 _game objects_ 를 관리하는 역할을 수행합니다. 예를 들어, 게임이 진행되면서 많은 객체들은 생성과 소멸을 반복하게 됩니다. 이러한 과정 속에서 _object controller_ 는 어떤 객체가 공격을 받았는지, 어떤 객체가 소멸되어야 하는지를 판단하고 알맞은 행동을 수행합니다. 

</br>

  - ## ObjectController.enroll()
    _**enroll method**_ 는 객체가 생성되었음을 관리자에게 알려줍니다. 모든 _game object_ 는 생성됨과 동시에 _object controller_ 의 _enroll method_ 를 호출합니다. 호출된 _enroll method_ 는 객체의 _team과 role_ 을 기준으로, _issueID method_ 를 호출하여 객체마다 고유한 identification을 발급합니다. 즉, _enroll_ 이 호출되면, 객체는 _team과 role_ 에 따라서 다르게 등록됩니다. 이 덕분에 player가 적군 비행기를 격추하거나 혹은 player가 공격 받는 경우를 명확히 파악할 수 있습니다.
    
  </br>
  
  - ## ObjectController.renew()
    
  

</br></br>

# Game Starter

</br></br>

