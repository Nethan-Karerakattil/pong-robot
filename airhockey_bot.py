import copy

# Bot Memory
ball_previous_pos = None

def bot(ball_pos, bat_pos, bat_height):
    global ball_previous_pos

    if ball_previous_pos is None:
        ball_previous_pos = copy.deepcopy(ball_pos)
        return 0

    # Calculate direction and speed of ball
    dx = ball_pos[0] - ball_previous_pos[0]
    dy = ball_pos[1] - ball_previous_pos[1]

    if dx < 0:
        ball_previous_pos = copy.deepcopy(ball_pos)
        return 0
    
    # Figure out where ball will be when it reaches the bat
    m = None
    collide_point = None
    
    if dy < 0:
        m = -1
    else:
        m = 1
    
    projected_ball = copy.deepcopy(ball_pos[1])

    dist = bat_pos[0] - ball_pos[0]
    for i in range(int(dist)):
        projected_ball += m

        if projected_ball <= 0 or projected_ball >= 512:
            m = -m

    collide_point = projected_ball

    # Move bat towards the ball
    ipt = 0

    if collide_point == bat_pos[1] + bat_height / 2:
        ipt = 0
    elif collide_point < bat_pos[1] + bat_height / 2:
        ipt = -1
    elif collide_point > bat_pos[1] + bat_height / 2:
        ipt = 1

    ball_previous_pos = copy.deepcopy(ball_pos)
    return ipt
