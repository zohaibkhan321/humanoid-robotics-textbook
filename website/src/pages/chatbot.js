import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Chatbot from '@site/src/components/Chatbot';

import Heading from '@theme/Heading';
import styles from './chatbot.module.css';

function ChatbotPageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.chatbotHeroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          Humanoid Robotics Assistant
        </Heading>
        <p className="hero__subtitle">
          Ask questions about humanoid robotics and get answers from the textbook content
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/module-4/rag-chatbot">
            Learn More About RAG Chatbot
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function ChatbotPage() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Humanoid Robotics Assistant`}
      description="Interactive chatbot for the Humanoid Robotics Textbook">
      <ChatbotPageHeader />
      <main className={styles.chatbotMain}>
        <div className={styles.chatbotContainer}>
          <div className={styles.chatbotWrapper}>
            <Chatbot />
          </div>
          <div className={styles.chatbotInfo}>
            <h2>How It Works</h2>
            <ul>
              <li>Ask questions about humanoid robotics in natural language</li>
              <li>The system retrieves relevant textbook content</li>
              <li>Answers are generated with proper citations to source material</li>
              <li>Get accurate, contextual responses based on the textbook</li>
            </ul>
            <h2>Tips for Best Results</h2>
            <ul>
              <li>Be specific with your questions</li>
              <li>Ask about concepts, techniques, or applications</li>
              <li>Request explanations of complex topics</li>
              <li>Ask for examples or use cases</li>
            </ul>
          </div>
        </div>
      </main>
    </Layout>
  );
}