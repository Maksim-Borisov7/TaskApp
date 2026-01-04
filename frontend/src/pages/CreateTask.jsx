import { Form, Input, Button, message } from "antd";
import { createTask } from "../api/tasks";

export default function CreateTask({ onCreated }) {
  const onFinish = async (values) => {
    try {
      await createTask(values);
      message.success("Задача создана");
      onCreated();
    } catch {
      message.error("Ошибка создания задачи");
    }
  };

  return (
    <Form layout="vertical" onFinish={onFinish}>
      <Form.Item name="title" label="Название" rules={[{ required: true }]}>
        <Input />
      </Form.Item>

      <Form.Item name="description" label="Описание">
        <Input.TextArea rows={15} />
      </Form.Item>

      <Button type="primary" htmlType="submit">Создать</Button>
    </Form>
  );
}
