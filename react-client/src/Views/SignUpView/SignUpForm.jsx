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

  const [secondPassword, setSecondPassword] = useState("");
  const [passwordMatch, setPasswordMatch] = useState(true);
  const [emailValid, setEmailValid] = useState(true);
  const [passwordValid, setPasswordValid] = useState(true);

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    const newUserDetail = { ...signUpDetails };
    newUserDetail[name] = value;
    setSignUpDetails(newUserDetail);
  };

  const checkPasswordMatch = (e) => {
    setPasswordMatch(secondPassword === signUpDetails.password);
  };

  const checkEmailIsValid = () => {
    if (!signUpDetails.email.includes("@")) {
      setEmailValid(false);
      return;
    }
    const address = signUpDetails.email.split("@");
    if (
      address.length !== 2 ||
      !address[0] ||
      !address[1] ||
      !address[1].includes(".")
    ) {
      setEmailValid(false);
      return;
    }
    setEmailValid(true);
  };

  const checkPasswordIsValid = () => {
    // Check whether password contains letter, number, character
    const strongPassword = new RegExp(
      "(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})"
    );
    setPasswordValid(strongPassword.test(signUpDetails.password));
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
        <div className="grid grid-cols-2 divide-x">
          <div className="grid grid-cols-1 gap-0 pr-6">
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
                onBlur={checkEmailIsValid}
              />
              <p
                className={`form-warning text-transparent ${
                  !emailValid && "text-red-500"
                }`}
              >
                아이디는 이메일 형식이여야 합니다.
              </p>
            </label>
            <label className="block mt-2">
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
              <p className="form-warning text-transparent">placeholder</p>
            </label>
          </div>
          <div className="grid grid-cols-1 gap-0 pl-6">
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
                onBlur={() => {
                  // checkPasswordMatch();
                  checkPasswordIsValid();
                }}
              />
              <p
                className={`form-warning text-transparent ${
                  !passwordValid && "text-red-500"
                }`}
              >
                영문, 숫자, 특수문자 포함 8자 이상이여야 합니다.
              </p>
            </label>
            <label className="block mt-2">
              <p className="text-gray-700 font-medium ml-1 mb-2.5">
                <span className="text-red-500 text-lg"> * </span>
                비밀번호 확인:
              </p>
              <input
                type="password"
                className="form-style"
                onChange={(e) => setSecondPassword(e.target.value)}
                onBlur={checkPasswordMatch}
              />
              <p
                className={`form-warning text-transparent ${
                  !passwordMatch && "text-red-500"
                }`}
              >
                비밀번호가 일치하지 않습니다.
              </p>
            </label>
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
