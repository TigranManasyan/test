# logging

'''
    1. DEBUG 
    2. INFO
    3. WARNING 
    4. ERROR 
    5. CRITICAL


'''

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename='app.log',
    filemode='a',
    encoding='utf-8'
)

# logging.debug('Debug հաղորդագրություն')
# logging.info('Info հաղորդագրություն')
# logging.warning('Warning հաղորդագրություն')
# logging.error('Warning հաղորդագրություն')
# logging.critical('Critical հաղորդագրություն')


try:
    print(10 / 0)
except ZeroDivisionError:
    logging.error("Թիվը զրոյի բաժանելչի կարելի")