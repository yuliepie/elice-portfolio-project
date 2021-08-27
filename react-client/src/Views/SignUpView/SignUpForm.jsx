import { useRef, useState } from "react";
import axios from "axios";
import { Link, useHistory } from "react-router-dom";
import { useAuth } from "../../Contexts/authContext";
import AlertModal from "../../Components/AlertModal";

export default function SignUpForm() {
  const { setCurrentUser } = useAuth();
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

  //==============
  // Modal Alert
  //==============
  const [showModal, setShowModal] = useState(false);
  const [modalContent, setModalContent] = useState({
    title: "",
    mainText: "",
    isAlert: true,
  });
  const [showModalButtons, setShowModalButtons] = useState(false);

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

  const tempUserData = useRef(null);
  const handleSignUp = async (e) => {
    e.preventDefault();
    const { email, password, name } = signUpDetails;

    if (!email || !password || !name) {
      setModalContent({
        mainText: "모든 항목을 입력해주세요.",
        isAlert: true,
      });
      setShowModal(true);
      return;
    }

    if (!passwordMatch) {
      setModalContent({
        mainText: "비밀번호가 일치하지 않습니다.",
        isAlert: true,
      });
      setShowModal(true);
      return;
    }

    try {
      const response = await axios.post("/api/users", signUpDetails);
      if (response) {
        console.log("user!");
        setModalContent({
          title: "회원가입 성공!",
          mainText: "지금 바로 포트폴리오를 설정하러 가시겠어요?",
          isAlert: false,
        });
        setShowModalButtons(true);
        setShowModal(true);
        tempUserData.current = response.data;
        console.log("user created.", signUpDetails);
      }
    } catch (e) {
      setModalContent({
        title: "회원가입 실패",
        mainText: "나중에 다시 시도해주세요.",
      });
    }
  };

  return (
    <div className="w-full">
      {/* Alert modal */}
      <AlertModal
        title={modalContent.title}
        mainText={modalContent.mainText}
        showModal={showModal}
        setShowModal={setShowModal}
        isAlert={modalContent.isAlert}
      >
        {showModalButtons && (
          <div className="grid grid-cols-2 gap-2 w-full">
            <button
              onClick={() => {
                setCurrentUser(tempUserData.current);
                history.push({
                  pathname: "/users/my-page",
                  state: { isEditing: true },
                });
              }}
              className="bg-indigo-500 p-2 rounded-full text-white text-lg h-full shadow-sm"
            >
              네!
            </button>
            <button
              className="bg-indigo-50 p-2 rounded-full text-indigo-900 font-normal h-full border border-indigo-300"
              onClick={() => {
                setCurrentUser(tempUserData.current);
                history.push("/");
              }}
            >
              아니요, 구경부터 할래요
            </button>
          </div>
        )}
      </AlertModal>

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
