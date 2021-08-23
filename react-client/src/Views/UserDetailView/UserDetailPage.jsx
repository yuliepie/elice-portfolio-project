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
  const [awards, setAwards] = useState(null);

  const createInitialState = () => {
    return {
      educations: [],
      awards: [],
    };
  };

  // Changed Details - for PATCH request
  const changedDetails = useRef(createInitialState());

  // New details - for POST request
  const newDetails = useRef(createInitialState());

  // API Fetch
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
  useEffect(() => {
    fetchUserDetails();
  }, []);

  // Checks Authorization for page editing
  const { currentUser } = useAuth();
  let { id } = useParams();

  const canEdit = useMemo(() => {
    return id == currentUser.id;
  }, [currentUser.id]);

  const [pageInEditMode, setPageInEditMode] = useState(false);
  const [boxesInEdit, setBoxesInEdit] = useState(0);

  //========================
  // Change Handlers
  //========================

  // Common Change Handler for all boxes
  const handleChange = (id, name, value, setState, newList, changedList) => {
    setState((prevList) => {
      return prevList.map((item) =>
        item.id === id ? { ...item, [name]: value } : item
      );
    });

    if (id[0] === "n") {
      // If NEW ITEM:
      const item = newList.filter((item) => item.id === id)[0];
      item[name] = value;
    } else {
      // If CHANGED ITEM:
      const item = changedList.filter((item) => item.id === id)[0];
      if (item) {
        item[name] = value;
      } else {
        changedList.push({
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

  const handleSave = () => {
    if (!boxesInEdit) {
      console.log("NEW: ");
      console.log(newDetails.current.educations);
      console.log("CHANGED:");
      console.log(changedDetails.current.educations);
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
        .then(() => alert("업데이트 성공!"))
        .catch((e) => alert("failed."))
        .then(() => {
          fetchUserDetails();
          newDetails.current = createInitialState();
          changedDetails.current = createInitialState();
        });

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
        <div className="inline-flex flex-col bg-yellow-200 flex-1 px-6 py-4 overflow-y-auto">
          <EducationsBox
            educations={educations}
            pageInEditMode={pageInEditMode}
            setBoxesInEdit={setBoxesInEdit}
            handleAdd={handleNewEducation}
            handleChange={(id, name, value) =>
              handleChange(
                id,
                name,
                value,
                setEducations,
                newDetails.current.educations,
                changedDetails.current.educations
              )
            }
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
