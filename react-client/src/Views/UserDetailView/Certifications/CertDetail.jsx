import parseDate from "../../../Helpers/DateParser";

export default function CertDetail({ cert }) {
  const acqDate = parseDate(cert.acquired_date);

  return (
    <div className="user-detail-wrapper">
      <h3 className="user-detail-title">
        {cert.name}
        <span className="float-right user-detail-date">{`${acqDate.year}년 ${acqDate.month}월 ${acqDate.day}일`}</span>
      </h3>
      <p className="user-detail-desc">{cert.provider}</p>
    </div>
  );
}
