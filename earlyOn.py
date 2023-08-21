import EarlyOnTable
import webbrowser



def main():
    table = EarlyOnTable.getHtmlTable()
    with open('earlyOn.html', 'w') as html_file:
        html_file.writelines(table)

    webbrowser.open('earlyOn.html', new=2)


if __name__ == "__main__":
    main()
