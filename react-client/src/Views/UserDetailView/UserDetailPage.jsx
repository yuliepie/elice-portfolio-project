import PageLayout from "../../Components/PageLayout";
import { useAuth } from "../../Contexts/authContext";
import axios from "axios";
import { useParams } from "react-router-dom";
import { useEffect, useMemo, useRef, useState } from "react";
import EducationsBox from "./Education/EducationsBox";
import EducationStatus from "./Education/EducationStatus";

export default function UserDetailPage() {
  const [description, setDescription] = useState(null);
  const [educations, setEducations] = useState(null);

  const changedDetails = useRef({
    educations: [],
  });
  const newDetails = useRef({
    educations: [],
  });

  // Update Handlers
  const handleEducationChange = (id, name, value) => {
    setEducations((prevEdus) => {
      return prevEdus.map((edu) =>
        edu.id === id ? { ...edu, [name]: value } : edu
      );
    });

    // Check if new/changed education:
    if (id[0] === "n") {
      const edu = newDetails.current.educations.filter(
        (edu) => edu.id === id
      )[0];
      edu[name] = value;
    } else {
      const edu = changedDetails.current.educations.filter(
        (edu) => edu.id === id
      )[0];
      if (edu) {
        edu[name] = value;
      } else {
        changedDetails.current.educations.push({
          id: id,
          [name]: value,
        });
      }
    }
  };

  const handleNewEducation = () => {
    const newEdu = {
      id: "n-" + new Date().getTime().toString(),
      school_name: "",
      major: "",
      status_id: "1",
      user_id: currentUser.id,
    };
    setEducations((prevEdus) => [...prevEdus, newEdu]);
    newDetails.current.educations.push(newEdu);
  };

  const { currentUser } = useAuth();
  let { id } = useParams();

  const canEdit = useMemo(() => {
    console.log("id match: ", id, currentUser.id);
    console.log(currentUser.email);
    return id == currentUser.id;
  }, [currentUser.id]);

  const [pageInEditMode, setPageInEditMode] = useState(false);
  const [boxesInEdit, setBoxesInEdit] = useState(0);

  async function fetchUserDetails() {
    try {
      const response = await axios.get(`/api/users/${id}`);
      const { user_details } = response.data;
      setEducations(user_details.educations);
      console.log(response.data);
      console.log(educations);
    } catch (e) {
      console.log("error in getting user details:", e.message);
    }
  }
  // Fetch user details
  useEffect(() => {
    fetchUserDetails();
  }, []);

  const handleSave = () => {
    if (!boxesInEdit) {
      // Axios post
      const promises = [];
      newDetails.current.educations.forEach((edu) => {
        const formattedEdu = [];
        formattedEdu.push(["school_name", edu.school_name]);
        formattedEdu.push(["major", edu.major]);
        formattedEdu.push(["status_id", parseInt(edu.status_id)]);
        promises.push(axios.post(`/api/users/${id}/educations`, formattedEdu));
      });

      changedDetails.current.educations.forEach((edu) => {
        promises.push(
          axios.patch(`/api/users/${id}/educations/${edu.id}`, edu)
        );
      });

      Promise.all(promises)
        .then(fetchUserDetails)
        .catch((e) => alert("failed."));

      setPageInEditMode(false);
    } else {
      alert("수정 완료되지 않은 항목이 있습니다.");
    }
  };

  return (
    <PageLayout>
      <div>User Details!!!</div>
      <div className="flex w-auto bg-red-200 h-full ml-24 mr-4 gap-4">
        <div className="inline-flex flex-col w-3/12 bg-green-200 px-8 py-4">
          <div className="w-full bg-gray-300 h-1/4">이미지</div>
        </div>
        <div className="inline-flex flex-col bg-yellow-200 flex-1 px-6 py-4">
          <EducationsBox
            educations={educations}
            pageInEditMode={pageInEditMode}
            setBoxesInEdit={setBoxesInEdit}
            handleAdd={handleNewEducation}
            handleChange={handleEducationChange}
          />
        </div>
        <div className="inline-flex flex-col bg-blue-200 w-min-content py-4 px-4">
          {canEdit && !pageInEditMode && (
            <button
              onClick={() => setPageInEditMode(true)}
              className="rounded-lg bg-red-200 w-20 h-12"
            >
              수정
            </button>
          )}
          {pageInEditMode && (
            <button
              onClick={handleSave}
              className="rounded-lg bg-red-200 w-20 h-12"
            >
              완료
            </button>
          )}
        </div>
      </div>
    </PageLayout>
  );
}
