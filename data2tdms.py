import numpy as np
from nptdms import TdmsFile, TdmsWriter, RootObject,ChannelObject

bg_red = 5
bg_green = 8
ratio_r2g = 0.649

name = input('please type in the file name:')
filename = 'C:\\Users\\86183\\Desktop\\' + name + '.tdms'
original_file = TdmsFile(filename)
original_groups = original_file.groups()
#这里用【3：】的原因是nptdms不能够直接替换数据，只会添加数据，所以要选取不变动的数据，其他数据进行直接添加
original_channels = [chan for group in original_groups for chan in group.channels()][3:]

chn_r = original_file['Data']['Pixel ch 1'][:] - bg_red
chn_g = original_file['Data']['Pixel ch 2'][:] - bg_green
chn_r = chn_r - chn_g * ratio_r2g
# chn_r = np.array([int(i) for i in chn_r])
chn_r = np.where(chn_r>0,chn_r,0)
# chn_g = np.array([int(i) for i in chn_g])
chn_g = np.where(chn_g>0,chn_g,0)
chn_b = original_file['Data']['Pixel ch 3'][:]
# chn_b = np.array([int(i) for i in chn_b])

# original_channels[0,:] = chn_r
#
# print (original_channels)
# print(len(chn_r))
with TdmsWriter('C:\\Users\\86183\\Desktop\\' + name + '-corrected' + '.tdms') as copied_file:
    root_object = RootObject(original_file.properties)
# 这里必须加号
    copied_file.write_segment([root_object]+original_groups)
    ch_1 = ChannelObject("Data", "Pixel ch 1", chn_r, properties={
    "Channel_name": 'Red',
    "NI_ArrayColumn": 7,
})
    ch_2 = ChannelObject("Data", "Pixel ch 2", chn_g, properties={
    "Channel_name": 'Green',
    "NI_ArrayColumn": 8,
})
    ch_3 = ChannelObject("Data", "Pixel ch 3", chn_b, properties={
        "Channel_name": 'Blue',
        "NI_ArrayColumn": 9,
    })
#这里必须逗号
    copied_file.write_segment([ch_1,ch_2,ch_3]+original_channels)

