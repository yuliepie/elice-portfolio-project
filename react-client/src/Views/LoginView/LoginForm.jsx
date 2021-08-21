import { Form, Input, Button, Checkbox } from "antd";

export default function LoginForm() {
  const formLayout = {
    // set size of label part, size of form part
    labelCol: { span: 8 },
    wrapperCol: { span: 8 },
  };

  const buttonLayout = {
    wrapperCol: { span: 8, offset: 8 },
  };

  const onFinish = (values) => {
    console.log("Login Success", values);
  };

  const onFinishFailed = (errorInfo) => {
    console.log("Login Fail", errorInfo);
  };

  return (
    <Form
      {...formLayout}
      name="login"
      onFinish={onFinish}
      onFinishFailed={onFinishFailed}
    >
      <Form.Item
        label="이메일 주소"
        name="email"
        rules={[
          {
            required: true,
            message: "이메일주소를 입력해 주세요!",
          },
        ]}
      >
        <Input />
      </Form.Item>

      <Form.Item
        label="비밀번호"
        name="password"
        rules={[
          {
            required: true,
            message: "비밀번호를 입력해 주세요!",
          },
        ]}
      >
        <Input.Password />
      </Form.Item>

      <Form.Item {...buttonLayout} className="centered">
        <Button type="primary" htmlType="submit">
          회원가입
        </Button>
      </Form.Item>
    </Form>
  );
}
