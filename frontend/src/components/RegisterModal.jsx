import React from "react";
import { Modal, Form, Input, Button, message } from "antd";
import { register } from "../services/api";

const RegisterModal = ({ visible, onCancel, onSwitchToLogin }) => {
  const [form] = Form.useForm(); 
    
  const handleRegister = async (values) => {
    form.resetFields()
    try {
      await register(values.email, values.password);
      message.success("Registration successful. Please verify your email before signing in.");
      onSwitchToLogin();
    } catch (error) {
      message.error(`Registration failed. ${error?.response?.data?.detail?.toString()}`);
    }
  };

  return (
    <Modal
      open={visible}
      onCancel={onCancel}
      footer={null}
      className="modal"
    >
        <h1>Register</h1>
      <Form form={form} onFinish={handleRegister} className="form">
        <Form.Item
          name="email"
          required={false}
          labelCol={{ span: 24 }}
          wrapperCol={{ span: 24 }}
          label="Email"
          rules={[
            { required: true, message: "Please input your email!" },
            { type: "email", message: "Please enter a valid email!" },
          ]}
          className="item"
        >
          <Input placeholder="Type email" className="input"/>
        </Form.Item>
        <Form.Item
          name="password"
          required={false}
          label="Password"
          labelCol={{ span: 24 }}
          wrapperCol={{ span: 24 }}
          className="item"
          rules={[{ required: true, message: "Please input your password!" }]}
        >
          <Input.Password placeholder="Type password" className="input"/>
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" className="modal-btn">
            Register
          </Button>
          <p className="link-text">
            Have an account?{" "}
            <span onClick={onSwitchToLogin} className="link">
              Login
            </span>
          </p>
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default RegisterModal;
