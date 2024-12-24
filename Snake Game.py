import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")

        
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="black")
        self.canvas.pack()

        
        self.snake = [(100, 100), (90, 100), (80, 100)]  
        self.snake_direction = "Right"
        self.food_position = self.place_food()
        self.score = 0

       
        self.score_text = self.canvas.create_text(50, 10, text=f"Score: {self.score}", fill="white", font=("Arial", 14))

        
        self.food = self.canvas.create_rectangle(
            self.food_position[0], self.food_position[1],
            self.food_position[0] + 10, self.food_position[1] + 10,
            fill="red"
        )

        
        self.snake_squares = [
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green")
            for x, y in self.snake
        ]

        
        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))

        
        self.run_game()

    def place_food(self):
        x = random.randint(0, 59) * 10
        y = random.randint(0, 39) * 10
        return x, y

    def change_direction(self, new_direction):
        opposite_directions = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_direction != opposite_directions.get(self.snake_direction):
            self.snake_direction = new_direction

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.snake_direction == "Up":
            head_y -= 10
        elif self.snake_direction == "Down":
            head_y += 10
        elif self.snake_direction == "Left":
            head_x -= 10
        elif self.snake_direction == "Right":
            head_x += 10

        
        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]

        
        if new_head == self.food_position:
            self.snake.append(self.snake[-1])  
            self.food_position = self.place_food()  
            self.canvas.coords(self.food, self.food_position[0], self.food_position[1], self.food_position[0] + 10, self.food_position[1] + 10)
            self.score += 1
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

        return new_head

    def check_collisions(self, head):
        x, y = head
        
        return (
            x < 0 or x >= 600 or y < 0 or y >= 400 or head in self.snake[1:]
        )

    def update_snake_graphics(self):
        for square, (x, y) in zip(self.snake_squares, self.snake):
            self.canvas.coords(square, x, y, x + 10, y + 10)

    def run_game(self):
        new_head = self.move_snake()
        if self.check_collisions(new_head):
            self.canvas.create_text(300, 200, text="Game Over", fill="red", font=("Arial", 24))
            return

        self.update_snake_graphics()
        self.root.after(100, self.run_game)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
