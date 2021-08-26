import UserDetailsBox from "../Shared/UserDetailsBox";
import ProjectDetail from "./ProjectDetail";
import ProjectForm from "./ProjectForm";
import { useState } from "react";

export default function ProjectsBox({
  projects,
  pageInEditMode,
  setBoxesInEdit,
  handleChange,
  handleAdd,
  validate,
}) {
  const [isEditing, setIsEditing] = useState(false);

  return (
    <UserDetailsBox
      title={"프로젝트"}
      pageInEditMode={pageInEditMode}
      isEditing={isEditing}
      setIsEditing={setIsEditing}
      setBoxesInEdit={setBoxesInEdit}
      handleAdd={handleAdd}
      validate={validate}
    >
      {projects &&
        (!isEditing
          ? projects.map((proj) => (
              <ProjectDetail key={proj.id} project={proj} />
            ))
          : projects.map((proj) => (
              <ProjectForm
                handleChange={handleChange}
                key={proj.id}
                project={proj}
              />
            )))}
    </UserDetailsBox>
  );
}
