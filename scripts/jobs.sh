case $1 in
    "build")
        python3 -m build
    ;;
    "deploy_test")
        twine upload --repository testpypi dist/*
    ;;
    "build_deploy_test")
        rm -rf dist/*
        python -m build
        twine upload --repository testpypi dist/*
    ;;
    *)
        echo 'Unknown command'
        return 1
    ;;
esac
