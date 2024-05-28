
from Physics import Table

def test_generate_initial_table_svg():
    table = Table()

    svg_content = table.initializeEntireTable()



    with open("initial_table_state.svg", "w") as svg_file:
        svg_file.write(svg_content)
    
    print("SVG content generated and saved to initial_table_state.svg. Please open this file in a browser to inspect the SVG visually.")

if __name__ == "__main__":
    test_generate_initial_table_svg()
