import pygame, random, sys, time

pygame.init()

# DISPLAY VARIABLES
s = 32
width , height = 12 * s, 20 * s
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Math Quiz")

# GAME VARIABLES
var1, var2 = 0, 0 # starting two operands
ans = 0
question = "Start"
r = 0  # Works as score and range for the game
started = False

# OPTIONS VARIABLES
correctOp = random.randint(0, 3)
options = [0,0,0,0]
chosenOption = None
chosen = False

# TIMER VARIABLES
t = 15  # time
clock = pygame.time.Clock() # frame rate
lastTime =  time.time() # for calculating change in time
timer = 0 # for calculating change in time
deltaTime = 0 # change in time
color = [(119,255,35), (255, 255, 90), (255, 113, 0), (255, 0, 0)] # Colors of the timer
index = 0 # indexing the color array

# FONT VARIABLE
font = pygame.font.Font("freesansbold.ttf", s) # font for all texts

""" DRAWING RECTANGLES """
def drawBoard(surface, index):
	global width, height, s, color

	#QUESTION
	pygame.draw.rect(surface, (255,255,255), (s, s, width - 2*s, height / 3))
	#OPTIONS
	pygame.draw.rect(surface, (255,255,255), (s, 2*s + height / 3, width / 2 - 3*s/2, height / 6))
	pygame.draw.rect(surface, (255,255,255), (width / 2 + s/2, 2*s + height / 3, width / 2 - 3*s/2, height / 6))
	pygame.draw.rect(surface, (255,255,255), (s, 3*s + height / 2, width / 2 - 3*s/2, height / 6))
	pygame.draw.rect(surface, (255,255,255), (width / 2 + s/2, 3*s + height / 2, width / 2 - 3*s/2, height / 6))
	#TIMER
	pygame.draw.rect(surface, color[index], (0, 4*s + 2*height / 3, width, 2*s))
	#SCORE
	pygame.draw.rect(surface, color[0], (s,s, 4*s, s))

""" RENDERING QUESTION AND THE OPTIONS """
def renderText(surface):
	global font, width, height, t

	""" TEXT VARIABLES """
	#QUESTION
	questionText = font.render(f"{question}", True, (0,0,0))
	#OPTIONS
	op1 = font.render(f"{options[0]}", True, (0,0,0))
	op2 = font.render(f"{options[1]}", True, (0,0,0))
	op3 = font.render(f"{options[2]}", True, (0,0,0))
	op4 = font.render(f"{options[3]}", True, (0,0,0))
	#TIME
	timeText = font.render(f"{t}", True, (0,0,0))
	#SCORE
	score = pygame.font.Font("freesansbold.ttf", int(s / 1.6)).render(f"Score: {r}", True, (0,0,0))
	
	""" RENDERING TEXT """
	#QUESTION
	surface.blit(questionText, ((width - questionText.get_rect().width) / 2, ((height / 3) - questionText.get_rect().height)/2 + s))
	#OPTIONS
	surface.blit(op1, (s/4 + (width / 2 - op1.get_rect().width)/2, 2*s + (5*height/6 - op1.get_rect().height)/2))
	surface.blit(op2, (3*width/4 - s/4 - op2.get_rect().width/2, 2*s + (5*height/6 - op2.get_rect().height)/2))
	surface.blit(op3, (s/4 + (width / 2 - op3.get_rect().width)/2, 3*s + 7*height / 12 - op3.get_rect().height/2))
	surface.blit(op4, (3*width/4 - s/4 - op4.get_rect().width/2, 3*s + 7*height / 12 - op4.get_rect().height/2))	
	#TIMER
	surface.blit(timeText, ((width - timeText.get_rect().width)/2, 5*s + 2*height/3 - timeText.get_rect().height/2))
	#SCORE
	surface.blit(score , (3*s - score.get_rect().width/2, 3*s/2 - score.get_rect().height/2))
	
""" GENERATING THE QUESTION WITH 5 OPERATIONS +-*/^ """
def genQuestion():
	global var1, var2, ans, r, question, options, correctOp
	var1 = random.randint(r, 2*r + 10)
	var2 = random.randint(r, 2*r + 10)
	operation = random.randint(1, 5)

	if operation == 1:
		ans = var1 + var2
		question = f"{var1} + {var2}"
	elif operation == 2:
		ans = var1 - var2
		question = f"{var1} - {var2}"
	elif operation == 3:
		ans = var1 * var2
		question = f"{var1} * {var2}"
	elif operation == 4:

		while var2 == 0:
			var2 = random.randint(r, 2*r + 10)
		while var1 / var2 != var1 // var2:
			while var2 == 0:
				var2 = random.randint(r, 2*r + 10)

		ans = var1 / var2
		question = f"{var1} / {var2}"
	elif operation == 5:
		var2 = random.randint(1,3)
		ans = var1 ** var2
		question = f"{var1} ^ {var2}"

	options[correctOp] = ans
	for i in range(4):
		if i != correctOp:
			move = random.randint(-10, 10)
			options[i] = ans + move

""" RESETING THE GAME WINDOW AFTER EVERY ANSWER """
def reset(message):
	global question, chosen, started, correctOp, options, chosenOption, t, timer, lastTime, deltaTime, index
	question = message
	chosen = False
	started = False
	correctOp = random.randint(0, 3)
	options = [0,0,0,0]
	chosenOption = None
	lastTime = 0
	timer = 0
	deltaTime = 0
	t = 15
	index = 0

while True:
	clock.tick(10)
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			sys.exit()

		""" USING ENTER TO START AND KEYPAD NUMBERS 7 9 1 3  OR  Q E A D
			TO SELECT THE OPTIONS """
		if e.type == pygame.KEYDOWN:
			if started and e.key == pygame.K_KP7 or e.key == pygame.K_q:
				chosen = True
				chosenOption = 0
			if started and e.key == pygame.K_KP9 or e.key == pygame.K_e:
				chosen = True
				chosenOption = 1
			if started and e.key == pygame.K_KP1 or e.key == pygame.K_a:
				chosen = True
				chosenOption = 2
			if started and e.key == pygame.K_KP3 or e.key == pygame.K_d:
				chosen = True
				chosenOption = 3
			if (not started) and e.key == pygame.K_RETURN:
				started = True
				lastTime = time.time()
				genQuestion()

		""" USING MOUSE CLICKS TO PLAY """
		mouse = pygame.mouse.get_pos()
		if started and e.type == pygame.MOUSEBUTTONDOWN and mouse[0] > s and mouse[1] > 2*s + height / 3 and mouse[0] < width / 2 - s/2 and mouse[1] < 2*s + height / 2:
			chosen = True
			chosenOption = 0
		if started and e.type == pygame.MOUSEBUTTONDOWN and mouse[0] > width / 2 + s/2 and mouse[1] > 2*s + height / 3 and mouse[0] < width - s and mouse[1] < 2*s + height / 2:
			chosen = True
			chosenOption = 1
		if started and e.type == pygame.MOUSEBUTTONDOWN and mouse[0] > s and mouse[1] > 3*s + height / 2 and mouse[0] < width / 2 - s/2 and mouse[1] < 3*s + 2*height / 3:
			chosen = True
			chosenOption = 2
		if started and e.type == pygame.MOUSEBUTTONDOWN and mouse[0] > width / 2 + s/2 and mouse[1] > 3*s + height / 2 and mouse[0] < width - s and mouse[1] < 2*height / 3 + 3*s:
			chosen = True
			chosenOption = 3
		if (not started) and e.type == pygame.MOUSEBUTTONDOWN and mouse[0] > s and mouse[1] > s and mouse[0] < width - s and mouse[1] < height / 3 + s:
			started = True
			lastTime = time.time()
			genQuestion()

	surface.fill((100, 39, 200))
	if chosen:
		if options[chosenOption] == ans:
			reset("Correct!!")
			r += 1
		else:
			reset("Wrong!!")
			r = 0

	if started:
		timer = time.time()
		deltaTime += timer - lastTime
		lastTime = timer

		if deltaTime > 1:
			deltaTime = 0
			t -= 1
		if t <= 11:		index = 1
		if t <= 7:		index = 2
		if t <= 3:		index = 3
		if t == 0:
			reset("TimeOut!!")
			r = 0

	drawBoard(surface, index)
	renderText(surface)

	pygame.display.update()
