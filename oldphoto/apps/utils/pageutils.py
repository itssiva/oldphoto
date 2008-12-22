# -*- coding: UTF-8 -*-
def gen_page_list(c_p, t_p, p_len):
    """
    c_p 当前页
    t_p 总页数
    p_len 显示页数

    需要信息，总记录数，当前页

    1..99
    1 2 3 4 5 6 .. 99
    减去 第一页 最后一页 总共 5页

    page >4
    123 4
    1..345

    x-1>3
    1 .. x-2 x-1 x

    t-x>3
    x x+1 x+2 .. totle_page
    <em>1</em>
    <a href="http://www.yeeyan.com/?page=2">2</a>
    """
    html=None
    per_count=c_p-1#前继页数
    next_count=t_p-c_p#后继页数
    if per_count<p_len:
        next_count=p_len+(p_len-per_count)
    if next_count<p_len:
        per_count=p_len+(p_len-next_count)

    per_ext=c_p>per_count
    if not per_ext:
        #第一页
        #...
        #x-2 x-1 x
        html='<a href="http://www.yeeyan.com/?page=2">2</a>&nbsp;<b>....</b>&nbsp;'
        html+=''
        pass
    else:
        for i in range(3):
            p=i+1
    #TODO 当前页
    next_ext=t_p-c_p>3
    pass