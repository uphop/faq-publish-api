eval "$(pyenv init -)" && pyenv local 3.7.9
python3 -m unittest discover -s ./tests/unit -p 'test_*.py' -v