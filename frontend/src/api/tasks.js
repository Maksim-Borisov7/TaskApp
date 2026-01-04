import api from "./axios";


export const getTasks = () => api.get("/task/get/");

export const toggleTaskState = (taskId) =>
  api.put(`/task/update/${taskId}`);

export const createTask = (data) => api.post("/task/create/", data);

export const deleteTask = (taskId) => api.delete(`/task/delete/${taskId}`);