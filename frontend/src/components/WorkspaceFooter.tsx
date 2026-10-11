import { translate as t, useI18n } from "../i18n";
import { BrandMark } from "./BrandMark";
import { Link, useLocation } from "react-router-dom";
import {
  ArrowRightIcon,
  ArrowTopRightIcon,
  EnvelopeClosedIcon,
  GitHubLogoIcon,
  PaperPlaneIcon,
} from "@radix-ui/react-icons";
import { BorderGlow } from "./design/BorderGlow";
import { projectInfo, projectSources, projectStack } from "../lib/projectInfo";
import "./WorkspaceFooter.css";

const footerNavigation = [
  { to: "/about", label: "About us" },
  { to: "/companies", label: "Companies" },
  { to: "/clusters", label: "Relationship groups" },
  { to: "/people", label: "People" },
  { to: "/contracts", label: "Contracts" },
] as const;

export function WorkspaceFooter() {
  useI18n();
  const { pathname } = useLocation();
  if (pathname !== "/about")
    return (
      <footer
        className="workspace-footer-compact"
        aria-label={t("Project information")}
      >
        <span>IZ2 · {t("Educational thesis prototype")}</span>
        <nav aria-label={t("Footer navigation")}>
          <Link to="/about">{t("About us")}</Link>
          <Link to="/about#contacts">{t("Get in touch")}</Link>
          <a href="/api/v1/docs/">{t("API documentation")}</a>
          <a
            href={projectInfo.repositoryUrl}
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
          <a
            href="/static/frontend/third-party-notices.txt"
            target="_blank"
            rel="noopener noreferrer"
          >
            {t("Component credits")}
          </a>
        </nav>
      </footer>
    );
  return (
    <footer
      className="workspace-footer-full"
      aria-label={t("Project information")}
    >
      <div className="workspace-footer-inner">
        <div className="workspace-footer-top">
          <div className="footer-project-intro">
            <Link
              to="/"
              className="footer-project-brand"
              aria-label={t("IZ2 overview")}
            >
              <BrandMark />
              <small>{t("EVIDENCE, CONNECTED")}</small>
            </Link>
            <p>
              {t(
                "A workspace for reviewing company relationships in Kazakhstan public procurement.",
              )}
            </p>
            <span className="footer-project-status">
              <i aria-hidden="true" /> {t("Educational thesis prototype")}
            </span>
            <Link to="/about" className="footer-about-link">
              {t("Meet the project")} <ArrowRightIcon aria-hidden="true" />
            </Link>
          </div>

          <nav className="footer-explore" aria-label={t("Footer navigation")}>
            <h2>{t("Explore the workspace")}</h2>
            <ul>
              {footerNavigation.map(({ to, label }) => (
                <li key={to}>
                  <Link to={to}>{t(label)}</Link>
                </li>
              ))}
            </ul>
            <a
              className="footer-api-link"
              href="/api/v1/docs/"
              target="_blank"
              rel="noopener noreferrer"
            >
              {t("API documentation")} <ArrowTopRightIcon aria-hidden="true" />
            </a>
          </nav>

          <section
            className="footer-project-credits"
            aria-labelledby="footer-credits-title"
          >
            <h2 id="footer-credits-title">{t("Project credits")}</h2>
            <dl>
              <div>
                <dt>{t("Developer")}</dt>
                <dd>{projectInfo.developer}</dd>
              </div>
              <div>
                <dt>{t("Related article author")}</dt>
                <dd>{projectInfo.articleAuthor}</dd>
              </div>
            </dl>
            <a
              className="footer-university-link"
              href={projectInfo.universityUrl}
              target="_blank"
              rel="noopener noreferrer"
            >
              {projectInfo.university}
              <ArrowTopRightIcon aria-hidden="true" />
            </a>
          </section>

          <BorderGlow
            as="section"
            id="contacts"
            className="footer-contact-panel"
            aria-labelledby="footer-contact-title"
            glowRadius={18}
            fillOpacity={0.08}
          >
            <h2 id="footer-contact-title">{t("Get in touch")}</h2>
            <p>{t("Questions about the project or its implementation?")}</p>
            <a
              className="footer-email-link"
              href={`mailto:${projectInfo.email}`}
            >
              <EnvelopeClosedIcon aria-hidden="true" />
              <span>{projectInfo.email}</span>
            </a>
            <div className="footer-article-contact">
              <span className="footer-contact-person">
                {t("Related article ·")} {projectInfo.articleAuthor}
              </span>
              <a
                className="footer-email-link"
                href={`mailto:${projectInfo.articleEmail}`}
              >
                <EnvelopeClosedIcon aria-hidden="true" />
                <span>{projectInfo.articleEmail}</span>
              </a>
            </div>
            <div className="footer-contact-links">
              <a
                href={projectInfo.repositoryUrl}
                target="_blank"
                rel="noopener noreferrer"
              >
                <GitHubLogoIcon aria-hidden="true" /> {t("GitHub")}{" "}
                <ArrowTopRightIcon aria-hidden="true" />
              </a>
              <a
                href={projectInfo.telegramUrl}
                target="_blank"
                rel="noopener noreferrer"
              >
                <PaperPlaneIcon aria-hidden="true" /> {t("Telegram")}{" "}
                <ArrowTopRightIcon aria-hidden="true" />
              </a>
            </div>
          </BorderGlow>
        </div>

        <div className="workspace-footer-resources">
          <section
            className="footer-source-section"
            aria-labelledby="footer-sources-title"
          >
            <h2 id="footer-sources-title">{t("Source services")}</h2>
            <ul>
              {projectSources.map(({ name, domain, url }) => (
                <li key={url}>
                  <a
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    title={t(name)}
                  >
                    {domain}
                    <ArrowTopRightIcon aria-hidden="true" />
                  </a>
                </li>
              ))}
            </ul>
            <p>{t("Stored results show availability and source dates.")}</p>
          </section>
          <section
            className="footer-stack-section"
            aria-labelledby="footer-stack-title"
          >
            <h2 id="footer-stack-title">{t("Built with")}</h2>
            <ul>
              {projectStack.map((technology) => (
                <li key={technology}>{technology}</li>
              ))}
            </ul>
          </section>
        </div>

        <div className="workspace-footer-bottom">
          <span>
            © {new Date().getFullYear()} {t("IZ2. Educational project.")}
          </span>
          <span>
            {t(
              "Evidence supports review. A relationship does not establish a violation.",
            )}
          </span>
          <a
            href="/static/frontend/third-party-notices.txt"
            target="_blank"
            rel="noopener noreferrer"
          >
            {t("Component credits")} <ArrowTopRightIcon aria-hidden="true" />
          </a>
        </div>
      </div>
    </footer>
  );
}

export default WorkspaceFooter;
