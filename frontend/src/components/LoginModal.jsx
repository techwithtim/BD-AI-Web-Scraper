import React from "react";
import { Modal, Form, Input, Button, message } from "antd";
import { useAuth } from "../contexts/AuthContext";
import "../css/LoginModal.css";

const LoginModal = ({ visible, onCancel, onSwitchToRegister }) => {
  const { login } = useAuth();
  const [form] = Form.useForm(); 

  const handleLogin = async (values) => {
    form.resetFields()
    try {
      await login(values.username, values.password);
      message.success("Login successful.");
      onCancel();
    } catch (error) {
      message.error(`Login failed. Please check your credentials and/or verify your email.`);
    }
  };

  return (
    <Modal
      open={visible}
      onCancel={onCancel}
      footer={null}
      className="modal"
    >
      <Form onFinish={handleLogin} className="form" form={form}>
        <h1>Login</h1>
        <Form.Item
          name="username"
          label="Email"
          required={false}
          labelCol={{ span: 24 }}
          wrapperCol={{ span: 24 }}
          rules={[{ required: true, message: "Please input your email!" }]}
          className="item"
        >
          <Input placeholder="Type email" className="input"/>
        </Form.Item>
        <Form.Item
          labelCol={{ span: 24 }}
          wrapperCol={{ span: 24 }}
          required={false}
          name="password"
          label="Password"
          rules={[{ required: true, message: "Please input your password!" }]}
          className="item"
        >
          <Input.Password placeholder="Type password" className="input" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" className="modal-btn">
            Login
          </Button>
          <p className="link-text">
            Don't have an account?{" "}
            <span onClick={onSwitchToRegister} className="link">
              Register
            </span>
          </p>
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default LoginModal;
