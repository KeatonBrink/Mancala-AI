all: pip-install

pip-install-local:
	cd prerequisites && make pip-install
	pip install -e .

build-go-agent:
	cd demo-agents/go_agent && go build

play-go-human-player0: build-go-agent
	cd demo-agents && python3 play.py go_human0

play-go-human-player1: build-go-agent
	cd demo-agents && python3 play.py go_human1

play-go-robots: build-go-agent
	cd demo-agents && python3 play.py

play-py-robots:
	cd demo-agents && python3 play.py py_robots

play-py-human-player0: build-go-agent
	cd demo-agents && python3 play.py py_human0

play-py-human-player1: build-go-agent
	cd demo-agents && python3 play.py py_human1
