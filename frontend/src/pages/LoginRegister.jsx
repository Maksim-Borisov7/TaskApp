import { useState } from "react";
import { Form, Input, Button, Card, Typography, message } from "antd";
import { UserOutlined, MailOutlined, LockOutlined } from "@ant-design/icons";
import axios from "axios";
import "../styles/auth.css";


export default function LoginRegister({ onLoginSuccess }) {
  const [mode, setMode] = useState("login"); 
  const [loading, setLoading] = useState(false);

  const handleRegister = async (values) => {
  setLoading(true);
  try {
    await axios.post("http://127.0.0.1:8000/auth/registration/", values);
    message.success("Регистрация успешна!");
    setMode("login");
  } catch (err) {
    if (err.response?.status === 409) {
      message.error("Пользователь уже существует");
    }
    else {
      message.error("Ошибка регистрации");
    }
  } finally {
    setLoading(false);
  }
};



  const handleLogin = async (values) => {
  setLoading(true);
  try {
    const formData = new FormData();
    formData.append("username", values.username);
    formData.append("password", values.password);

    const response = await axios.post(
      "http://127.0.0.1:8000/auth/login/",
      formData,
      { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
    );

    localStorage.setItem("token", response.data.access_token);
    message.success("Вход выполнен!");
    onLoginSuccess();
  } catch (err) {
    if (err.response?.status === 401) {
      message.error("Неверный логин или пароль");
    } else {
      message.error("Ошибка авторизации");
    }
  } finally {
    setLoading(false);
  }
};



  return (
    <div className="auth-container">
      <Card className="auth-card">
        <div className="logo">TaskApp</div>

        <Typography.Title level={3} style={{ textAlign: "center" }}>
          {mode === "login" ? "Вход" : "Регистрация"}
        </Typography.Title>

        {mode === "register" && (
          <Form layout="vertical" onFinish={handleRegister} className="fade">
            <Form.Item
              label="Логин"
              name="username"
              rules={[
                { required: true, message: "Введите логин" },
                { type: "string", min: 3, max: 20, message: "Логин должен быть от 3 до 20 символов" }
              ]}
            >
              <Input size="large" prefix={<UserOutlined />} placeholder="Введите логин" />
            </Form.Item>

            <Form.Item
              label="Email"
              name="email"
              rules={[
                { required: true, message: "Введите email" },
                { type: "email", message: "Некорректный email" }
              ]}
            >
              <Input size="large" prefix={<MailOutlined />} placeholder="Введите email" />
            </Form.Item>

            <Form.Item
              label="Пароль"
              name="password"
              rules={[
                { required: true, message: "Введите пароль" },
                { type: "string", min: 3, max: 20, message: "Логин должен быть от 3 до 20 символов" }
              ]}
            >
              <Input.Password size="large" prefix={<LockOutlined />} placeholder="Введите пароль" />
            </Form.Item>

            <Button type="primary" htmlType="submit" size="large" block loading={loading}>
              Зарегистрироваться
            </Button>

            <div className="switch" onClick={() => setMode("login")}>
              Уже есть аккаунт? Войти
            </div>
          </Form>
        )}

        {mode === "login" && (
          <Form layout="vertical" onFinish={handleLogin} className="fade">
            <Form.Item
              label="Логин"
              name="username"
              rules={[{ required: true, message: "Введите логин" }]}
            >
              <Input size="large" prefix={<UserOutlined />} placeholder="Введите логин" />
            </Form.Item>

            <Form.Item
              label="Пароль"
              name="password"
              rules={[{ required: true, message: "Введите пароль" }]}
            >
              <Input.Password size="large" prefix={<LockOutlined />} placeholder="Введите пароль" />
            </Form.Item>

            <Button type="primary" htmlType="submit" size="large" block loading={loading}>
              Войти
            </Button>

            <div className="switch" onClick={() => setMode("register")}>
              Нет аккаунта? Зарегистрироваться
            </div>
          </Form>
        )}
      </Card>
    </div>
  );
}

