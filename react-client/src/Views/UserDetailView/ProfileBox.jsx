import { useState } from "react";
import EditItemButton from "./Shared/EditItemButton";

export default function ProfileBox({
  pageInEditMode,
  setBoxesInEdit,
  name,
  description,
  handleProfileChange,
}) {
  const [isEditing, setIsEditing] = useState(false);

  return (
    <div
      className={
        pageInEditMode
          ? "user-profile-box bg-indigo-50 bg-opacity-90 border-gray-700 border-opacity-50 shadow-2xl"
          : "user-profile-box border-transparent"
      }
    >
      <div className="w-48 h-48 rounded-full bg-detail-profile-img bg-contain shadow-2xl" />
      {!isEditing ? (
        <>
          <h3
            className={`mt-6 text-4xl font-bold shared-transition ${
              pageInEditMode ? "text-gray-800" : "text-white"
            }`}
          >
            {name}
          </h3>
          <p
            className={`mt-3 text-base font-medium shared-transition ${
              pageInEditMode ? "text-gray-700" : "text-indigo-50"
            }`}
          >
            {description}
          </p>
        </>
      ) : (
        <div className="w-full px-2 mt-4 flex flex-col items-center">
          <input
            type="text"
            className="details-form-style py-0.5 text-center"
            placeholder="이름"
            value={name}
            name="name"
            onChange={handleProfileChange}
          />
          <input
            type="text"
            className="details-form-style text-center w-full py-1"
            required
            placeholder="한줄소개"
            value={description}
            name="description"
            onChange={handleProfileChange}
          />
        </div>
      )}

      {pageInEditMode && !isEditing && (
        <EditItemButton
          handleClick={() => {
            setIsEditing(true);
            setBoxesInEdit((prev) => prev + 1);
          }}
          position="absolute -top-2 -right-2"
        />
      )}
      {isEditing && (
        <>
          {/* 수정완료 버튼 */}
          <button
            onClick={() => {
              const isValid = name && description;
              if (isValid) {
                setIsEditing(false);
                setBoxesInEdit((prev) => prev - 1);
              } else {
                alert("모든 항목을 입력하세요.");
              }
            }}
            className="edit-btn text-sm p-2 rounded-lg absolute -top-2 right-2 text-white shadow-lg transition duration-200 ease-in-out"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        </>
      )}
    </div>
  );
}
