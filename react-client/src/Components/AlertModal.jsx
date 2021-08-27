import { useState } from "react";

export default function AlertModal({
  title,
  isAlert,
  mainText,
  showModal,
  setShowModal,
  children,
}) {
  return (
    <div
      className={`fixed z-30 flex justify-center left-0 top-0 w-full h-full bg-gray-300 bg-opacity-0 ${
        showModal ? "bg-opacity-60 visible" : "bg-opacity-0 invisible"
      }`}
      id="modal-parent"
      onClick={(e) => {
        if (e.target.id === "modal-parent") {
          setShowModal(false);
        }
      }}
    >
      <div
        className={`relative flex flex-col items-center bg-gray-50 mx-auto my-28 py-4 px-8 border-gray-300 border rounded-2xl shadow-lg transition duration-300 ease-in-out transition-all ${
          !showModal ? "transform scale-0" : "transform scale-100"
        } ${isAlert ? "h-1/3 w-3/12" : "h-1/3 w-4/12"}`}
      >
        {isAlert && (
          <span
            className="text-gray-900 self-end absolute top-3 right-4 cursor-pointer hover:text-gray-400"
            onClick={() => setShowModal(false)}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
          </span>
        )}
        {title && (
          <h3 className="text-2xl text-gray-800 font-bold border-b border-gray-400 w-full text-center pb-2">
            {title}
          </h3>
        )}
        <p className="my-auto text-lg text-gray-900">{mainText}</p>
        <div className="w-full">{children}</div>
      </div>
    </div>
  );
}
