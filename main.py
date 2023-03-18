from Ticket.ticket import Ticket
# from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':

    with Ticket() as bot:
        bot.getMainPage()
        bot.change_currency(currency='TRY')
        bot.select_departure(loc_from="İzmir")
        bot.select_destination(loc_to="Antalya")
        bot.select_departure_date("2023-03-18")
        bot.search_ticket()