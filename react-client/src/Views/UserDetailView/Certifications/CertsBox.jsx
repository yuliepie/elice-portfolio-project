import UserDetailsBox from "../Shared/UserDetailsBox";
import CertDetail from "./CertDetail";
import CertForm from "./CertForm";
import { useState } from "react";

export default function CertsBox({
  certs,
  pageInEditMode,
  setBoxesInEdit,
  handleChange,
  handleAdd,
  validate,
  handleDelete,
}) {
  const [isEditing, setIsEditing] = useState(false);

  return (
    <UserDetailsBox
      title={"자격증"}
      pageInEditMode={pageInEditMode}
      isEditing={isEditing}
      setIsEditing={setIsEditing}
      setBoxesInEdit={setBoxesInEdit}
      handleAdd={handleAdd}
      validate={validate}
    >
      {certs &&
        (!isEditing
          ? certs.map((cert) => <CertDetail key={cert.id} cert={cert} />)
          : certs.map((cert) => (
              <CertForm
                handleChange={handleChange}
                key={cert.id}
                cert={cert}
                handleDelete={() => handleDelete(cert.id)}
              />
            )))}
    </UserDetailsBox>
  );
}
