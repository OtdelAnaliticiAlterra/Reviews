"""
{
"ajax" : "1",
"businessId" : "1133310706",
"csrfToken" : "74c6d6fcd1c6b614621a6bcf4b7fb283b4f54b64%3A1732676131",
"locale" : "ru_RU",
"page" : "2",
"pageSize" : "50",
"ranking" : "by_relevance_org",
"reqId" : "1732676131285421-3200110675-addrs-upper-yp-42",
"s" : "2846096157",
"sessionId" : "1732676131259796-1357853185052782690-balancer-l7leveler-",
}

"""
from yandex_reviews_parser.utils import YandexParser
id_ya = 1133310706 #ID Компании Yandex
parser = YandexParser(id_ya)

all_data = parser.parse()

print(all_data)