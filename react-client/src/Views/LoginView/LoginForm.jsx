import { useState } from "react";
import { Link, useHistory } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../../Contexts/authContext";

export default function LoginForm() {
  const history = useHistory();
  const { setCurrentUser } = useAuth();
  const [loginDetails, setLoginDetails] = useState({ email: "", password: "" });

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    const newLoginDetail = { ...loginDetails };
    newLoginDetail[name] = value;
    setLoginDetails(newLoginDetail);
  };

  const handleLoginSubmit = (e) => {
    e.preventDefault();

    axios
      .post("/api/login", loginDetails)
      .then((response) => {
        const { user } = response.data;
        console.log("user logged in: ", user);
        alert("로그인 성공!");

        setCurrentUser(user);
        history.push("/");
      })
      .catch((err) => {
        console.log(err);
        alert("잘못된 비밀번호입니다.");
      });
  };
  return (
    <div>
      <div>
        <form className="my-4">
          <div className="grid grid-cols-1 gap-6">
            <label className="block">
              <span className="text-gray-700">아이디 (이메일):</span>
              <input
                name="email"
                type="email"
                className="form-style"
                placeholder="john@example.com"
                required
                onChange={handleInputChange}
              />
            </label>
            <label className="block">
              <span className="text-gray-700">비밀번호:</span>
              <input
                name="password"
                type="password"
                className="form-style"
                required
                onChange={handleInputChange}
              />
            </label>
            <button
              type="subimit"
              className="bg-blue-200 w-20 p-2 mx-auto"
              onClick={handleLoginSubmit}
            >
              로그인
            </button>
          </div>
        </form>
        <div className="text-center">
          <Link to="/signup" className="w-max-content">
            <span className="border-b-2 border-blue-500 w-max-content text-blue-500">
              아직 회원이 아니신가요?
            </span>
          </Link>
        </div>
      </div>
    </div>
  );
}
