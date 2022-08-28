
from cgitb import handler
import PySimpleGUI as sg
import base64

from .views import *
from .event_handler import parse_event


class FrontEndMain():

    result_toolkit = None
    window = None
    current_view = ""
    #Result data
    result_data = ""

    def __init__(self, result_toolkit, result_data):
        #Set the assessment toolkit
        self.result_toolkit = result_toolkit   
        self.result_data = result_data 

        

    def make_window(self,theme):
        sg.theme(theme)
  
        layout = view_container(self)

        directory = os.getcwd() 
        # print("directory cwd :: " + directory)
        icon=base64.b64encode(open(directory+"/frontend/img/car-results-icon.png", 'rb').read())
        window = sg.Window(
            'Results : Assessment Toolkit For Safe Self Driving Cars', 
            layout, 
            # grab_anywhere=True, 
            resizable=True, 
            margins=(0,0), 
            # use_custom_titlebar=True, 
            # min_size=(200,300),
            finalize=True, 
            keep_on_top=False,
            icon=icon
            )
       
        window.TKroot.minsize(400,900)
        # window.set_min_size(window.size)
        
        return window

    def get_current_scenario_name(self):
        return self.result_toolkit.get_current_scenario_name()

    def get_current_view(self):
        return self.current_view

    def refresh_window_data(self):
        self.window.layout = view_container()
        self.change_view(self.current_view)



    def create_plot(self):
        year = [2021,2020,3033,331]
        unemployment_rate = [9,8,2,2.5]
        plt.plot(year, unemployment_rate, color='blue', marker='o')
        plt.title("Unemployment Rate vs Year", fontsize=14) 
        plt.xlabel('Year', fontsize=14)
        plt.ylabel('Unemployment Rate', fontsize=14)
        plt.grid(True)
        return plt.gcf()

    def draw_figure(self,canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    def start(self):
        window = self.make_window(sg.theme("Reddit"))
        #Set the window to be accessed later. 
        self.window = window
        

        # This is an Event Loop 
        while True:       
            
            event = parse_event(self.window)
            
            if(event["event_name"] =="close_window"):
                #Window Close Event if event_handler.run(window,event,values) RETURNS "close_window"
                break      
            

            if(event['event_name'] == 'open_result_from_summary_table'):
                scenario_name = self.result_data.get_all_process_result_available_scenarios()[event['scenario_index'][0]]
                #self.draw_figure(self.window['-CANVAS-'].TKCanvas, self.create_plot())
                self.change_view('view_results_page_'+scenario_name)

        window.close()
        exit(0)
    
    






    #Change the GUI view
    def change_view(self,target_view):
        print("gui: change_view : ", target_view)

        available_views = [
            "view_results_main_menu",
            "view_results_page_follow_vehicle",
            "view_results_page_pedestrian_crossing",
            "view_results_page_red_light"
            "view_results_page_intersection_left_turn"
        ]


        if target_view in available_views:
            
            for view in available_views:
                if(view == target_view):
                    self.window[view].update(visible=True)
                    self.current_view = target_view
                else:
                    self.window[view].update(visible=False)
            
            return True
          
       
    def set_view_result_data(self, result_data): 
        print('Loading results into the GUI...')

    


        
    def get_result_data(self):
        return self.result_data


