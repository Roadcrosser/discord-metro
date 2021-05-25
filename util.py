EJECT_SYMBOL = "\U000023cf\U0000fe0f"


def draw_map(curr_ind, nxt_ind, direction, max_num, transit, looped):
    node_icon = "\U0001f7e0"
    curr_icon = "\U0001f535"
    dir_icon = ["\U000025c0\U0000fe0f", None, "\U000025b6\U0000fe0f"][direction + 1]
    joiner_symbol = "\U00002796"

    min_stage = min(curr_ind, nxt_ind)
    valid_transition = curr_ind + direction == nxt_ind  # without loops in mind

    s_map = ""

    for i in range(max_num):
        if (not transit) and i == curr_ind:
            s_map += curr_icon
        else:
            s_map += node_icon

        if i != max_num - 1:

            if transit and i == min_stage and valid_transition:
                s_map += dir_icon
            else:
                s_map += joiner_symbol

    if looped:
        loop_symbol = joiner_symbol
        if not valid_transition:
            loop_symbol = dir_icon

        s_map = loop_symbol + s_map + loop_symbol

    return s_map


def has_role(member, role):
    return role.id in [r.id for r in member.roles]
