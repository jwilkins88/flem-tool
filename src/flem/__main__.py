if __name__ == "__main__":
    import sys

    # from pathlib import Path

    print(sys.path)

    # sys.path.insert(0, Path(__file__).parent.as_posix())
    from flem.cli.flem_tool import main

    main()
