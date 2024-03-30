#pragma once

#include <cstdint>

namespace REFrameworkNET {
ref struct InvokeRet;

public interface class IProxyable {
    void* Ptr();
    uintptr_t GetAddress();

    bool HandleInvokeMember_Internal(System::String^ methodName, array<System::Object^>^ args, System::Object^% result);
};
}