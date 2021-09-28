# data_management.py
'''
    Compare the all tested  to tge liat of isam with no messages
    ISAM still communicating = Total ISAM tested - ISAM with no message
'''

# ***** Na atharraich dad nas fhaide an seo ******
def remove_no_message_isam(all_test_isam, no_message_isam):
    for x in no_message_isam:
        if x in all_test_isam:
            all_test_isam.remove(x)
    return all_test_isam
