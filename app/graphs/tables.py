from shiny import render


def register_table_outputs(input, output, session, filtered_data):
    """
    Registers table rendering functions.
    Tables in Shiny are rendered using the @render.table decorator,
    which automatically formats pandas DataFrames for display.
    """
    
    @output
    @render.table
    def statistics_table():
        """
        Renders a preview table of the filtered data.
        The @render.table decorator handles DataFrame formatting automatically.
        """
        data = filtered_data()
        return data.head()

