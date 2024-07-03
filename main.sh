isInvalid=false;

if [[ $# -eq 1 ]]
then
    if [[ "$1" == "run" ]]
    then
        python ./main.py;
    elif [[ "$1" == "test" ]]
    then
        python -m unittest discover -s ./tests;
    else
        isInvalid=true;
    fi
else
    isInvalid=true;
fi

if $isInvalid
then
    echo "usage: main.sh <command>";
    echo "";
    echo "Command list:";
    echo "run - run main program";
    echo "test - test main program against test cases";
fi
