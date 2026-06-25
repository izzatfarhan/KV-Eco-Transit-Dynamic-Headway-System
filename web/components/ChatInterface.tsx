"use client";

import { useState } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Bot, Send, User } from "lucide-react";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hello Operator. You can query the transit database using natural language, or ask me to generate a crisis broadcast alert.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { id: Date.now().toString(), role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Simulate API call to LangGraph backend
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "This is a mocked response from the AI Engine. Once the backend is connected, I will return the results of your Text-to-SQL query or the generated broadcast.",
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1500);
  };

  return (
    <Card className="flex flex-col h-[500px] w-full">
      <CardHeader className="border-b pb-4">
        <CardTitle className="flex items-center gap-2 text-xl font-semibold">
          <Bot className="h-6 w-6 text-primary" />
          Operator AI Assistant
        </CardTitle>
      </CardHeader>
      
      <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex items-start gap-3 ${msg.role === "user" ? "flex-row-reverse" : ""}`}
          >
            <div className={`p-2 rounded-full flex-shrink-0 ${msg.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted text-foreground"}`}>
              {msg.role === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
            </div>
            <div
              className={`p-3 rounded-xl max-w-[80%] text-sm ${
                msg.role === "user"
                  ? "bg-primary text-primary-foreground rounded-tr-none"
                  : "bg-muted text-foreground rounded-tl-none"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-full bg-muted text-foreground flex-shrink-0">
              <Bot className="h-4 w-4" />
            </div>
            <div className="p-3 rounded-xl bg-muted text-foreground rounded-tl-none text-sm flex gap-1">
              <span className="w-2 h-2 rounded-full bg-primary/50 animate-bounce"></span>
              <span className="w-2 h-2 rounded-full bg-primary/50 animate-bounce delay-75"></span>
              <span className="w-2 h-2 rounded-full bg-primary/50 animate-bounce delay-150"></span>
            </div>
          </div>
        )}
      </CardContent>

      <CardFooter className="border-t p-4 pt-4">
        <form 
          className="flex w-full items-center space-x-2" 
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
        >
          <Input
            type="text"
            placeholder="Type your query..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
            className="flex-1"
          />
          <Button type="submit" size="icon" disabled={isLoading || !input.trim()}>
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </CardFooter>
    </Card>
  );
}
