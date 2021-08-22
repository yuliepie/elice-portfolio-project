import { useState } from "react";
import axios from "axios";
import { useHistory } from "react-router";

export default function SignUpForm() {
  const history = useHistory();
  const [signUpDetails, setSignUpDetails] = useState({
    email: "",
    password: "",
    name: "",
  });

  const [passwordMatch, setPasswordMatch] = useState(true);

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    const newUserDetail = { ...signUpDetails };
    newUserDetail[name] = value;
    setSignUpDetails(newUserDetail);
  };

  const checkPasswordMatch = (e) => {
    setPasswordMatch(e.target.value === signUpDetails.password);
  };

  const handleSignUp = async (e) => {
    e.preventDefault();
    console.log(signUpDetails);

    try {
      const response = await axios.post("/api/users", signUpDetails);
      if (response) {
        alert("회원가입 성공!");
        console.log("user created.", signUpDetails);
        history.push("/login");
      }
    } catch (e) {
      alert("회원가입 실패");
    }
  };

  return (
    <div>
      <div>
        <form onSubmit={handleSignUp}>
          <div className="grid grid-cols-1 gap-6">
            <label className="block">
              <span className="text-gray-700">아이디 (이메일):</span>
              <input
                type="email"
                className="form-style"
                placeholder="john@example.com"
                required
                name="email"
                onChange={handleInputChange}
              />
            </label>
            <label className="block">
              <span className="text-gray-700">비밀번호:</span>
              <input
                type="password"
                className="form-style"
                required
                name="password"
                placeholder="최소 8자 이상."
                onChange={handleInputChange}
              />
            </label>
            <label className="block">
              <span className="text-gray-700">비밀번호 확인:</span>
              <input
                type="password"
                className="form-style"
                required
                onBlur={checkPasswordMatch}
              />
            </label>
            {!passwordMatch ? <p>비밀번호가 일치하지 않습니다.</p> : null}

            <label className="block">
              <span className="text-gray-700">이름:</span>
              <input
                type="text"
                name="name"
                className="form-style"
                required
                onChange={handleInputChange}
              />
            </label>
            <button
              type="submit"
              className="bg-blue-200 w-content-max p-2 mx-auto"
            >
              가입 완료하기
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
