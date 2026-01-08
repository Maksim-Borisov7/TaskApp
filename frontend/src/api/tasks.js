import api from "./axios";


export const getTasks = () => api.get("/tasks/get/");

export const toggleTaskState = (taskId) =>
  api.put(`/tasks/update/${taskId}`);

export const createTask = (data) => api.post("/tasks/create/", data);

export const deleteTask = (taskId) => api.delete(`/tasks/delete/${taskId}`);