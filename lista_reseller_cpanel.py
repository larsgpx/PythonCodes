import sys
from os import listdir, path



def get_list(srvbck_path):
    curlist = [f for f in listdir(srvbck_path) if path.isdir('%s/%s' % (srvbck_path, f) )]
    return curlist


def return_reseller_users(srvbck_path, fulllist,reseller):
    finallist = []
    for cur_user in fulllist:
        cur_file = '%s/%s/cp/%s' % (srvbck_path, cur_user, cur_user)
        try:
            conf = open(cur_file, 'r')
            if 'RESELLER=%s' % cur_user in conf.readall():
                finallist.insert(cur_user)
            conf.close()


    return finallist

dirlist =  get_list('/Users/lgarcia')
path = '/home/resellers/'
print return_reseller_users(path,get_list(path),)