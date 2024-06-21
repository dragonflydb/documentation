import React, { useCallback, useEffect, useState } from "react";

import ComponentTypes from "@theme-original/Footer/LinkItem";
import type FooterLinkType from "@theme/Footer/LinkItem";
import submitHubspotForm from "@site/src/utils/submitHubspotForm";
import Newsletter from "./Newsletter";
import Community from "./Community";

type Props = React.ComponentProps<typeof FooterLinkType>;

export default function FooterLink(props: Props): JSX.Element {
  const isAnnouncmentBar = props.item.type === "custom-announcmentBar";

  if (isAnnouncmentBar) {
    return <AnnouncmentBar />;
  }

  return <ComponentTypes {...props} />;
}

const AnnouncmentBar = () => {
  const [isOpen, setIsOpen] = useState(true);

  const showPopup = useCallback(() => {
    if (!sessionStorage.getItem("announcmentBarShown")) {
      sessionStorage.setItem("announcmentBarShown", "true");
      setIsOpen(true);
    }
  }, []);

  const showPopupBasedOnScroll = useCallback(() => {
    const scrolledPercentage =
      (window.scrollY /
        (document.documentElement.scrollHeight - window.innerHeight)) *
      100;
    if (scrolledPercentage > 20) {
      setIsOpen(true);
    }
  }, []);

  useEffect(() => {
    if (sessionStorage.getItem("announcmentBarShown")) return;

    window.addEventListener("scroll", showPopupBasedOnScroll);
    const timerId = setTimeout(showPopup, 5000);

    return () => {
      clearTimeout(timerId);
      window.removeEventListener("scroll", showPopupBasedOnScroll);
    };
  });

  if (isOpen) {
    return (
      <div className="announcment-bar">
        <Community />
        <button className="close-button" onClick={() => setIsOpen(false)}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="15"
            height="15"
            viewBox="0 0 15 15"
            fill="none"
          >
            <g>
              <path
                d="M4 11.875L3.125 11L6.625 7.5L3.125 4L4 3.125L7.5 6.625L11 3.125L11.875 4L8.375 7.5L11.875 11L11 11.875L7.5 8.375L4 11.875Z"
                fill="white"
              />
            </g>
          </svg>
        </button>
      </div>
    );
  }

  return null;
};
