import { useState } from "react";
import UserDetailsBox from "../UserDetailsBox";
import EducationDetail from "./EducationDetail";
import EducationForm from "./EducationForm";

export default function EducationsBox({
  educations,
  pageInEditMode,
  setBoxesInEdit,
  handleChange,
  handleAdd,
}) {
  const [isEditing, setIsEditing] = useState(false);
  const validate = () => {
    let isValid = true;
    educations.forEach((edu) => {
      for (const prop in edu) {
        if (!edu[prop]) {
          isValid = false;
          break;
        }
      }
    });
    return isValid;
  };

  return (
    <UserDetailsBox
      title={"학력"}
      pageInEditMode={pageInEditMode}
      isEditing={isEditing}
      setIsEditing={setIsEditing}
      setBoxesInEdit={setBoxesInEdit}
      handleAdd={handleAdd}
      validate={validate}
    >
      {educations &&
        (!isEditing
          ? educations.map((edu) => (
              <EducationDetail key={edu.id} education={edu} />
            ))
          : educations.map((edu) => (
              <EducationForm
                handleChange={handleChange}
                key={edu.id}
                education={edu}
              />
            )))}
    </UserDetailsBox>
  );
}
