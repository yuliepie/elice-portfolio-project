import { useState } from "react";
import AwardDetail from "./AwardDetail";
import AwardForm from "./AwardForm";
import UserDetailsBox from "../Shared/UserDetailsBox";

export default function AwardsBox({
  awards,
  pageInEditMode,
  setBoxesInEdit,
  handleChange,
  handleAdd,
  validate,
  handleDelete,
  setShowModal,
  setModalContent,
}) {
  const [isEditing, setIsEditing] = useState(false);

  return (
    <UserDetailsBox
      title={"수상 경력"}
      pageInEditMode={pageInEditMode}
      isEditing={isEditing}
      setIsEditing={setIsEditing}
      setBoxesInEdit={setBoxesInEdit}
      handleAdd={handleAdd}
      validate={validate}
      setShowModal={setShowModal}
      setModalContent={setModalContent}
    >
      {awards &&
        (!isEditing
          ? awards.map((award) => <AwardDetail key={award.id} award={award} />)
          : awards.map((award) => (
              <AwardForm
                handleChange={handleChange}
                key={award.id}
                award={award}
                handleDelete={() => handleDelete(award.id)}
              />
            )))}
    </UserDetailsBox>
  );
}
