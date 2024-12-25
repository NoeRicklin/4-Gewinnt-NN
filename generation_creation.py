from NN_Setup import bot_count
surv_num = 20
offset_range = 0.1

def next_generation(prev_generation, win_list):
    indices = [i for i in range(len(win_list))]
    win_ind = zip(win_list, indices)
    sorted_indices = [i[1] for i in sorted(win_ind, reverse=True)]

    survivors = sorted_indices[:surv_num]
    next_generation = [prev_generation[i] for i in survivors]
    for i in range(bot_count - surv_num):
        child = make_child(prev_generation[survivors[i % surv_num]])
        next_generation.append(child)