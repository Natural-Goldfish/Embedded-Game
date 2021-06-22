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

    - ### Enemy Object
      _**Enemy object**_ 는 player가 격추해야 하는 적군 전투기를 의미하며, 모든 _enemy object_ 는 체력을 의미하는 _hp_ 와 공격 주기를 의미하는 _attack_cycle_ 를 attribute로 가지고 있습니다. _Enemy object_ 가 공격을 시도하는 경우, _enemy object_ 가 바라보는 방향으로 _5 pixel_ 떨어진 위치에 _missile object_ 를 생성합니다. _Enemy object<sub>i</sub>_ 는 _name_ attribute 가 _missile<sub>i</sub>_ 인 _missile object_ 를 생성합니다. _Enemy<sub>i</sub>(index=i)_ 에 대한 관련 정보를 요약한 표는 다음과 같습니다:
      
      </br>
      
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
      
    - ### Player Object
      _**Player object**_ 는 player가 사용하는 전투기를 의미합니다. 체력을 의미하는 _hp_ 와 격추한 적군 전투기의 개수를 의미하는 _kill_point_ 를 attribute로 가지고 있습니다. _Player object_ 가 공격을 시도하는 경우, _player object_ 가 바라보는 방향으로 _5 pixel_ 떨어진 위치에 _missile object_ 를 생성합니다. _Player object<sub>i</sub>_ 는 _name_ attribute 가 _player-missile<sub>i</sub>_ 인 _missile object_ 를 생성합니다.  _Player<sub>i</sub>(index=i)_ 에 대한 관련 정보를 요약한 표는 다음과 같습니다:

      </br>
      
      <div align='center'>
      
      |Index|Fighter Plane|HP|Speed(x, y)|Missile|Damage|
      |:---:|:---:|:---:|:---:|:---:|:---:|
      |1|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/player1.png?raw=true" alt="player1" width="60" height="60"/>|20|(10, 10)|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/player-missile1.png?raw=true" alt="player-missile1" width="60" height="60"/>|15|
    
      </div>

    </br>

    - ### Missile Object
      _**Missile object**_ 는 _player object_ 혹은 _enemy object_ 가 사용하는 공격 수단을 의미하며, 모든 _missile object_ 는 공격력을 의미하는 _damage_ 를 attribute로 가지고 있습니다. 모든 _missile object_ 는 고유한 _name_ 을 가지고 있으며, _name_ 의 접두사 및 접미사를 기준으로 어떤 _player object_ 혹은 _enemy object_ 가 사용하는 _missile object_ 인지 구분할 수 있습니다.

    </br>

    - ### Effect-Boom Object
      _**Effect-Boom object**_ 는 전투기가 공격받고 폭파되는 경우 생성되는 effect 객체입니다. _Effect-Boom<sub>i</sub>(index=i)_ 에 대한 관련 정보를 요약한 표는 다음과 같습니다:

      </br>

      <div align='center'>
      
      |Index|Effect Boom|
      |:---:|:---:|
      |1|<img src="https://github.com/Natural-Goldfish/Shooting-Game/blob/main/images/effect-boom1.png?raw=true" alt="effect-boom1" width="60" height="60"/>|
    
      </div>

  </br>

  - ## Background Object
    _**Background object**_ 는 배경화면을 display하는 객체를 의미하며, 관련 내용은 `src/background.py`에 정의되어 있습니다. 모든 background object와 관련된 정보는 _**BACKGROUND_INFO**_ 에 있습니다. 앞서 설명한 game object의 이미지는 background object가 _call_ 됐을 때, background object가 가진 배경 이미지에 덧붙여집니다. _Background<sub>i</sub>(index=i)_ 에 대한 관련 정보를 요약한 표는 다음과 같습니다:

      </br>

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
    _**enroll method**_ 는 객체가 생성되었음을 관리자에게 알려줍니다.  
    
    모든 _game object_ 는 생성됨과 동시에 _object controller_ 의 _enroll method_ 를 호출합니다. 호출된 _enroll method_ 는 객체의 _team과 role_ 을 기준으로 _issueID method_ 를 호출하여, 객체마다 고유한 identification을 발급합니다. 즉, _enroll_ 이 호출되면, 객체는 _team과 role_ 에 따라서 다르게 등록됩니다. 이 덕분에 _object controller_ 는 전투기가 격추되는 경우나 공격받는 경우 등, 다양한 상황속에서도 해당 객체를 정확히 구별할 수 있습니다.
    
  </br>
  
  - ## ObjectController.renew()
    _**renew method**_ 는 객체들의 행동 및 상태를 관리합니다.
    
    </br>
    
    - ### 행동(Behavior)
      본 프로젝트에서의 행동은 크게 세 가지로 나누어집니다. 첫 번째는 player가 미사일을 발사합니다. Player가 _shoot button_ 을 클릭한 경우, _missile object_ 를 생성합니다. 두 번째는 적군 비행기가 미사일을 발사합니다. _OBJECT_INFO_ 에 정의된 _attack-cycle_ 조건을 만족한다면, _enemy object_ 가 _missile object_ 를 생성합니다. 세 번째는 모든 객체가 이동합니다. 모든 객체가 가지고 있는 고유의 _speed_ 값을 기준으로 객체를 이동시킵니다.

    </br>
    
    - ### 상태(State)
      상태 또한 크게 세 가지로 나눌 수 있습니다. 객체끼리 충돌한 경우와 충돌하지 않은 경우 그리고 화면 밖으로 객체가 이동한 상태입니다. 객체의 충돌을 판단하는 기준은 _IOU(intersection over union)_ 를 사용하며, 객체 상호간의 _IOU_ 가 0이상인 경우를 충돌한 것으로 판정합니다. 객체가 화면 밖으로 나가는 것을 판단하는 기준은 _object.obj_coord_ 인 객체의 중심 좌표를 기준을 사용하며, _object_ 에 따라 처리 방법이 상이합니다. _Enemy object_ 는 좌측, 우측 그리고 상단에 위치한 상태에서 화면 밖으로 이동할 경우에는 진행 방향을 reverse하여 화면 내부로 다시 진입하지만, 화면의 하단으로 이동한 경우에는 화면 내부로 다시 진입하지 않고 소멸됩니다. _Missile object_ 는 화면 밖으로 이동했을 때, 바로 소멸됩니다.
  
</br></br>

# Game Starter

</br></br>

