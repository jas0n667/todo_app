<template>
  <div class="todo-app">
    <h1 class="title">To-Do List</h1>
    <form @submit.prevent="addTodo" class="todo-form">
      <input
        v-model="newTodo.title"
        placeholder="Название задачи"
        required
        class="todo-input"
      />
      <input
        v-model="newTodo.description"
        placeholder="Описание (необязательно)"
        class="todo-input"
      />
      <button type="submit" class="add-button">Добавить</button>
    </form>

    <ul class="todo-list">
      <li v-for="todo in todos" :key="todo.id" class="todo-item">
        <span :class="{ completed: todo.completed }" class="todo-text">
          {{ todo.title }} - {{ todo.description }}
        </span>
        <div class="todo-buttons">
          <button @click="toggleComplete(todo)" class="complete-button">✔</button>
          <button @click="deleteTodo(todo.id)" class="delete-button">❌</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import apiClient from '../api';

export default {
  data() {
    return {
      todos: [],
      newTodo: {
        title: '',
        description: '',
      },
    };
  },
  methods: {
    async fetchTodos() {
      try {
        const response = await apiClient.get('/todos/');
        this.todos = response.data;
      } catch (error) {
        console.error('Ошибка загрузки задач:', error);
      }
    },
    async addTodo() {
      try {
        const response = await apiClient.post('/todos/', this.newTodo);
        this.todos.push(response.data);
        this.newTodo = { title: '', description: '' }; // Очистка формы
      } catch (error) {
        console.error('Ошибка добавления задачи:', error);
      }
    },
    async deleteTodo(id) {
      try {
        await apiClient.delete(`/todos/${id}`);
        this.todos = this.todos.filter((todo) => todo.id !== id);
      } catch (error) {
        console.error('Ошибка удаления задачи:', error);
      }
    },
    async toggleComplete(todo) {
      try {
        const response = await apiClient.put(`/todos/${todo.id}`, {
          completed: !todo.completed,
        });
        const index = this.todos.findIndex((t) => t.id === todo.id);
        this.todos[index] = response.data;
      } catch (error) {
        console.error('Ошибка обновления статуса задачи:', error);
      }
    },
  },
  mounted() {
    this.fetchTodos();
  },
};
</script>

<style>
/* Основной контейнер приложения */
.todo-app {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

.title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 20px;
  color: #333;
}

.todo-form {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.todo-input {
  padding: 10px;
  margin-bottom: 10px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
}

.add-button {
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-button:hover {
  background-color: #45a049;
}

/* Список задач */
.todo-list {
  list-style-type: none;
  padding: 0;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  padding: 15px;
  margin: 10px 0;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.todo-text {
  flex: 1;
  font-size: 1rem;
  color: #333;
}

.completed {
  text-decoration: line-through;
  color: #999;
}

/* Кнопки для задач */
.todo-buttons {
  display: flex;
  gap: 10px;
}

.complete-button,
.delete-button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.complete-button {
  background-color: #4caf50;
  color: white;
}

.complete-button:hover {
  background-color: #45a049;
}

.delete-button {
  background-color: #f44336;
  color: white;
}

.delete-button:hover {
  background-color: #e53935;
}
</style>
