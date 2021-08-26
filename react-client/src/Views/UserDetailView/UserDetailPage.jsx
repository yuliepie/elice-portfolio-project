import PageLayout from "../../Components/PageLayout";
import { useAuth } from "../../Contexts/authContext";
import axios from "axios";
import { useParams } from "react-router-dom";
import { useEffect, useMemo, useRef, useState } from "react";
import EducationsBox from "./Education/EducationsBox";
import AwardsBox from "./Awards/AwardsBox";
import ProjectsBox from "./Projects/ProjectsBox";
import CertsBox from "./Certifications/CertsBox";

export default function UserDetailPage({ myPage }) {
  const [description, setDescription] = useState(null);
  const [name, setName] = useState(null);
  const [educations, setEducations] = useState(null);
  const [awards, setAwards] = useState(null);
  const [projects, setProjects] = useState(null);
  const [certs, setCerts] = useState(null);

  const createInitialState = () => {
    return {
      educations: [],
      awards: [],
      projects: [],
      certs: [],
    };
  };

  const changedDetails = useRef(createInitialState()); // Changed Details - for PATCH request
  const newDetails = useRef(createInitialState()); // New details - for POST request

  // API Fetch
  let { id } = useParams();
  const { currentUser } = useAuth();
  const searchId = myPage ? currentUser.id : id;

  async function fetchUserDetails() {
    try {
      const response = await axios.get(`/api/users/${searchId}`);
      const { user_details } = response.data;
      setDescription(user_details.description);
      setEducations(user_details.educations);
      setAwards(user_details.awards);
      setProjects(user_details.projects);
      setCerts(user_details.certifications);
      setName(user_details.name);
    } catch (e) {
      console.log("error in getting user details:", e.message);
    }
  }
  useEffect(() => {
    fetchUserDetails();
  }, [searchId]);

  const [pageInEditMode, setPageInEditMode] = useState(false);
  const [boxesInEdit, setBoxesInEdit] = useState(0);

  // Validation check that forms are filled
  const validate = (collection) => {
    let isValid = true;
    collection.forEach((item) => {
      for (const prop in item) {
        if (!item[prop]) {
          isValid = false;
          break;
        }
      }
    });
    return isValid;
  };

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
    };
    setEducations((prevEdus) => [...prevEdus, newEdu]);
    newDetails.current.educations.push(newEdu);
  };

  const handleNewAward = () => {
    const newAward = {
      id: "n-" + new Date().getTime().toString(),
      name: "",
      description: "",
    };
    setAwards((prevAwards) => [...prevAwards, newAward]);
    newDetails.current.awards.push(newAward);
  };

  const handleNewProject = () => {
    const newProj = {
      id: "n-" + new Date().getTime().toString(),
      name: "",
      description: "",
      start_date: "",
      end_date: "",
    };
    setProjects((prevProjs) => [...prevProjs, newProj]);
    newDetails.current.projects.push(newProj);
  };

  const handleNewCert = () => {
    const newCert = {
      id: "n-" + new Date().getTime().toString(),
      name: "",
      provider: "",
      acquired_date: "",
    };
    setCerts((prevCerts) => [...prevCerts, newCert]);
    newDetails.current.certs.push(newCert);
  };

  //===================
  // ON SAVE
  //===================

  const handleSave = () => {
    if (!boxesInEdit) {
      // Check something has changed
      const {
        educations: newEdu,
        awards: newAward,
        projects: newProj,
        certs: newCert,
      } = newDetails.current;
      const nothingToPost =
        !newEdu.length &&
        !newAward.length &&
        !newProj.length &&
        !newCert.length;

      const {
        educations: changedEdu,
        awards: changedAward,
        projects: changedProj,
        certs: changedCert,
      } = changedDetails.current;
      const nothingToPatch =
        !changedEdu.length &&
        !changedAward.length &&
        !changedProj.length &&
        !changedCert.length;

      if (nothingToPost && nothingToPatch) {
        setPageInEditMode(false);
        return;
      }

      //--------
      // POST:
      //--------
      const promises = [];

      newDetails.current.educations.forEach((edu) => {
        const formattedEdu = [];
        formattedEdu.push(["school_name", edu.school_name]);
        formattedEdu.push(["major", edu.major]);
        formattedEdu.push(["status_id", parseInt(edu.status_id)]);
        promises.push(
          axios.post(`/api/users/${searchId}/educations`, formattedEdu)
        );
      });

      newDetails.current.awards.forEach((award) => {
        const formattedAward = [];
        formattedAward.push(["name", award.name]);
        formattedAward.push(["description", award.description]);
        promises.push(
          axios.post(`/api/users/${searchId}/awards`, formattedAward)
        );
      });

      newDetails.current.projects.forEach((proj) => {
        const formattedProj = [];
        formattedProj.push(["name", proj.name]);
        formattedProj.push(["description", proj.description]);
        formattedProj.push(["start_date", proj.start_date]);
        formattedProj.push(["end_date", proj.end_date]);
        promises.push(
          axios.post(`/api/users/${searchId}/projects`, formattedProj)
        );
      });

      newDetails.current.certs.forEach((cert) => {
        const formattedCert = [];
        formattedCert.push(["name", cert.name]);
        formattedCert.push(["provider", cert.provider]);
        formattedCert.push(["acquired_date", cert.acquired_date]);
        promises.push(
          axios.post(`/api/users/${searchId}/certifications`, formattedCert)
        );
      });

      //---------
      // PATCH:
      //---------

      changedDetails.current.educations.forEach((edu) => {
        promises.push(
          axios.patch(`/api/users/${searchId}/educations/${edu.id}`, edu)
        );
      });

      changedDetails.current.awards.forEach((award) => {
        promises.push(
          axios.patch(`/api/users/${searchId}/awards/${award.id}`, award)
        );
      });

      changedDetails.current.projects.forEach((proj) => {
        promises.push(
          axios.patch(`/api/users/${searchId}/projects/${proj.id}`, proj)
        );
      });

      changedDetails.current.certs.forEach((cert) => {
        promises.push(
          axios.patch(`/api/users/${searchId}/certifications/${cert.id}`, cert)
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
      <div className="fixed inset-x-0 top-20 pt-10 h-full w-4/12 bg-indigo-400">
        <div
          className={
            pageInEditMode
              ? "user-profile-box border-gray-700"
              : "user-profile-box border-transparent"
          }
        >
          <div className="w-48 h-48 rounded-full bg-detail-profile-img bg-contain shadow-2xl" />
          <h3 className="mt-6 text-white text-4xl font-bold">{name}</h3>
          <p className="mt-3 text-indigo-50 text-base font-medium">
            {description}
          </p>
        </div>
      </div>
      <div className="user-details w-5/12 flex flex-col bg-opacity-20 flex-1 py-10 pl-16  overflow-y-auto">
        <EducationsBox
          educations={educations}
          pageInEditMode={pageInEditMode}
          setBoxesInEdit={setBoxesInEdit}
          handleAdd={handleNewEducation}
          validate={() => validate(educations)}
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
        <AwardsBox
          awards={awards}
          pageInEditMode={pageInEditMode}
          setBoxesInEdit={setBoxesInEdit}
          handleAdd={handleNewAward}
          validate={() => validate(awards)}
          handleChange={(id, name, value) =>
            handleChange(
              id,
              name,
              value,
              setAwards,
              newDetails.current.awards,
              changedDetails.current.awards
            )
          }
        />
        <ProjectsBox
          projects={projects}
          pageInEditMode={pageInEditMode}
          setBoxesInEdit={setBoxesInEdit}
          handleAdd={handleNewProject}
          validate={() => validate(projects)}
          handleChange={(id, name, value) =>
            handleChange(
              id,
              name,
              value,
              setProjects,
              newDetails.current.projects,
              changedDetails.current.projects
            )
          }
        />
        <CertsBox
          certs={certs}
          pageInEditMode={pageInEditMode}
          setBoxesInEdit={setBoxesInEdit}
          handleAdd={handleNewCert}
          validate={() => validate(certs)}
          handleChange={(id, name, value) =>
            handleChange(
              id,
              name,
              value,
              setCerts,
              newDetails.current.certs,
              changedDetails.current.certs
            )
          }
        />
      </div>
      <div className="fixed inset-y-20 right-0 w-3/12 h-full flex flex-col py-4 px-10 justify-start items-start">
        {myPage && !pageInEditMode && (
          <button
            onClick={() => setPageInEditMode(true)}
            className="edit-btn p-2.5"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
            </svg>
          </button>
        )}
        {pageInEditMode && (
          <button onClick={handleSave} className="finish-btn p-2.5">
            완료
          </button>
        )}
      </div>
    </PageLayout>
  );
}
