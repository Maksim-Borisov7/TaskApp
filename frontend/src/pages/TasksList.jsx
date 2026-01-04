import { useEffect, useState } from "react";
import { Card, Tag, Button, Space, Spin, message, Flex } from "antd";
import { CheckCircleTwoTone, CloseCircleTwoTone, DeleteOutlined } from "@ant-design/icons";
import { getTasks, toggleTaskState, deleteTask } from "../api/tasks";
import { Popconfirm } from "antd";

export default function TasksList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadTasks = () => {
    setLoading(true);
    getTasks()
      .then((r) => setTasks(r.data))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleToggle = async (id) => {
    try {
      const r = await toggleTaskState(id);
      message.success(r.data.msg);
      loadTasks();
    } catch {
      message.error("Ошибка изменения состояния");
    }
  };

  const handleDelete = async (id) => {
    try {
      const r = await deleteTask(id);
      message.success(r.data.msg);
      loadTasks();
    } catch {
      message.error("Ошибка удаления задачи");
    }
  };

  if (loading) return <Spin size="large" style={{ marginTop: 50 }} />;

  return (
    <div style={{ padding: 30 }}>
      <h1 style={{ marginBottom: 20 }}>Список всех задач ↓</h1>

      <Flex vertical gap={16}>
        {tasks.map((task) => (
          <Card
            key={task.id}
            style={{
              borderRadius: 12,
              boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
            }}
            title={
              <Space>
                {task.is_done ? (
                  <CheckCircleTwoTone twoToneColor="#52c41a" />
                ) : (
                  <CloseCircleTwoTone twoToneColor="#ff4d4f" />
                )}
                <span>{task.title}</span>
              </Space>
            }
            extra={
              <Tag color={task.is_done ? "green" : "red"}>
                {task.is_done ? "Выполнена" : "Не выполнена"}
              </Tag>
            }
          >
            <p style={{ marginBottom: 20 }}>
              {task.description || "Описание отсутствует"}
            </p>

            <Space>
              <Button
                type={task.is_done ? "default" : "primary"}
                onClick={() => handleToggle(task.task_id)}
              >
                {task.is_done ? "Отметить как невыполненную" : "Отметить выполненной"}
              </Button>

              <Popconfirm
                title="Удалить задачу?"
                description="Вы уверены, что хотите удалить эту задачу?"
                okText="Да"
                cancelText="Нет"
                onConfirm={() => handleDelete(task.task_id)}
              >
                <Button danger icon={<DeleteOutlined />}>
                  Удалить
                </Button>
              </Popconfirm>
            </Space>
          </Card>
        ))}
      </Flex>
    </div>
  );
}
