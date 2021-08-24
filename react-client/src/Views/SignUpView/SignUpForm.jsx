import { useState } from "react";
import axios from "axios";
import { Link, useHistory } from "react-router-dom";

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
    const { email, password, name } = signUpDetails;

    if (!email || !password || !name) {
      alert("모든 항목을 입력해주세요.");
      return;
    }

    if (!passwordMatch) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }

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
    <div className="w-full">
      <form onSubmit={handleSignUp} className="mt-4">
        <div className="flex divide-x justify-center items-start">
          <div className="grid grid-cols-1 gap-4 flex-grow pr-6">
            <label className="block">
              <p className="text-gray-700 font-medium ml-1 mb-2.5">
                <span className="text-red-500 text-lg"> * </span>
                아이디 (이메일):
              </p>
              <input
                type="email"
                className="form-style"
                placeholder="john@example.com"
                name="email"
                onChange={handleInputChange}
              />
            </label>
            <label className="block">
              <p className="text-gray-700 font-medium ml-1 mb-2.5">
                <span className="text-red-500 text-lg"> * </span>
                이름:
              </p>
              <input
                type="text"
                name="name"
                className="form-style"
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="grid grid-cols-1 gap-4 flex-grow pl-6">
            <label className="block">
              <p className="text-gray-700 font-medium ml-1 mb-2.5">
                <span className="text-red-500 text-lg"> * </span>
                비밀번호:
              </p>
              <input
                type="password"
                className="form-style"
                name="password"
                placeholder="최소 8자 이상."
                onChange={handleInputChange}
              />
            </label>
            <label className="block">
              <p className="text-gray-700 font-medium ml-1 mb-2.5">
                <span className="text-red-500 text-lg"> * </span>
                비밀번호 확인:
              </p>
              <input
                type="password"
                className="form-style"
                onBlur={checkPasswordMatch}
              />
            </label>
            {!passwordMatch ? (
              <p className="justify-self-end mr-1 text-sm text-red-500">
                비밀번호가 일치하지 않습니다.
              </p>
            ) : null}
          </div>
        </div>
        <div className="grid grid-cols-1">
          <button type="submit" className="main-btn mt-10 mx-auto py-2.5 px-5">
            가입 완료
          </button>
        </div>
      </form>
      <div className="text-center mt-2">
        <Link to="/login" className="w-max-content">
          <span className="border-b-2 border-blue-500 w-max-content text-blue-500 text-sm">
            이미 회원이에요!
          </span>
        </Link>
      </div>
    </div>
  );
}
