#pragma once
#include <utility>
#include <xsd/cxx/tree/elements.hxx>
#include <xsd/cxx/tree/types.hxx>

namespace faulttree
{
	class Visitor;
}

namespace fuzztree
{
	class Visitor;
}

template <typename Base>
class FaultTreeVisitable : public Base
{
public:
	template <typename ...Args>
	FaultTreeVisitable(Args&&... args) : Base(std::forward<Args>(args) ...) {};

	virtual FaultTreeVisitable<Base>*
		_clone (::xsd::cxx::tree::flags f = 0, ::xsd::cxx::tree::type* c = 0) const
	{
		return new FaultTreeVisitable<Base>(*this, f, c);
	};

	// Implementation in Visitor.h
	virtual void accept(faulttree::Visitor& visitor);     
};


template <typename Base>
class FuzzTreeVisitable : public Base
{
public:
	template <typename ...Args>
	FuzzTreeVisitable(Args&&... args) : Base(std::forward<Args>(args) ...) {};


	virtual FuzzTreeVisitable<Base>*
		_clone (::xsd::cxx::tree::flags  f = 0, ::xsd::cxx::tree::type* c = 0) const
	{
		return new FuzzTreeVisitable<Base>(*this, f, c);
	};

	// Implementation in Visitor.h
	virtual void accept(fuzztree::Visitor& visitor);     
};